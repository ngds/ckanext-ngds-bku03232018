from ckan.plugins import toolkit
from ckanext.harvest.model import HarvestObject
from shapely.geometry import asShape
from pylons import config
import json
from dateutil import parser as date_parser


def render_jinja2(template_name, extra_vars):
    """Render a Jinja2 template without all the CKAN mumbo-jumbo in toolkit.render"""
    env = config['pylons.app_globals'].jinja_env
    template = env.get_template(template_name)
    return template.render(**extra_vars)


def get_harvested_content(package_id, context):
    """Check if a pacakge was harvested"""

    # This is lifted from ckanext-harvest plugin.py:before_view. Looks for a HarvestObject to go with your package
    harvest_object = context["model"].Session.query(HarvestObject) \
                    .filter(HarvestObject.package_id==package_id) \
                    .filter(HarvestObject.current==True) \
                    .first()
    if harvest_object:
        return harvest_object.content
    else:
        return None


def iso_metadata(context, data_dict):
    """
    Serialize a CKAN Package as an ISO 19139 XML document

    Gets the package to be converted, processes it, and passes it through a Jinja2 template
    which generates an XML string

    @param context: CKAN background noise
    @param data_dict: Must contain an "id" key which is a pointer to the package to serialize
    @return: ISO19139 XML string
    """

    package_id = data_dict.get("id", "")
    p = toolkit.get_action("package_show")(context, {"id": package_id})

    # NOTE: If this is a harvested package, we should just return the XML, without alteration
    #   ... but we can't figure out if it was harvested if no context is passed in
    harvested_content = None
    ngds_type = config.get("ngds.deployment", "node")
    if context is not None and ngds_type == "central":
        harvested_content = get_harvested_content(package_id, context)

    if harvested_content:
        output = harvested_content

    else:
        # ---- Reformat extras so they can be looked up
        p["additional"] = {}
        for extra in p["extras"]:
            p["additional"][extra["key"]] = extra["value"]

        # ---- Remove milliseconds from metadata dates
        p["metadata_modified"] = date_parser.parse(p.get("metadata_modified", "")).replace(microsecond=0).isoformat()
        p["metadata_created"] = date_parser.parse(p.get("metadata_created", "")).replace(microsecond=0).isoformat()

        # ---- Make sure that there is a publication date (otherwise you'll get invalid metadata)
        if not p["additional"].get("publication_date", False):
            p["additional"]["publication_date"] = p["metadata_created"]

        # ---- Figure out URIs
        other_ids = p["additional"].get("other_id", "[]")
        if len(json.loads(other_ids)) > 0:
            p["additional"]["datasetUri"] = json.loads(other_ids)[0]
        else:
            p["additional"]["datasetUri"] = config.get("ckan.site_url", "http://default.ngds.com").rstrip("/") + \
                "/dataset/%s" % p["name"]

        # ---- Load the authors
        authors = p["additional"].get("authors", None)
        try:
            p["additional"]["authors"] = json.loads(authors)
        except:
            p["additional"]["authors"] = [{"name": p["author"], "email": p["author_email"]}]

        # ---- Load Location keywords
        location = p["additional"].get("location", "[]")
        try:
            loc = json.loads(location)
            if not isinstance(loc, list):
                p["additional"]["location"] = [loc]
            else:
                p["additional"]["location"] = loc
        except:
            p["additional"]["location"] = []

        # ---- Reformat facets
        faceted_ones = [t for t in p.get("tags", []) if t.get("vocabulary_id") is not None]
        p["additional"]["facets"] = {}
        for faceted_tag in faceted_ones:
            vocab = toolkit.get_action("vocabulary_show")(None, {"id": faceted_tag.get("vocabulary_id", "")})
            vocab_name = vocab.get("name", None)
            if vocab_name is not None and vocab_name in p["additional"]["facets"]:
                p["additional"]["facets"][vocab_name].append(faceted_tag.get("display_name"))
            elif vocab_name is not None:
                p["additional"]["facets"][vocab_name] = [faceted_tag.get("display_name")]

        # ---- Extract BBOX coords from extras
        p["extent"] = {}

        geojson = p["additional"].get("spatial", None)

        if geojson is not None:
            try:
                bounds = asShape(json.loads(geojson)).bounds
                p["extent"] = {
                    "west": bounds[0],
                    "south": bounds[1],
                    "east": bounds[2],
                    "north": bounds[3]
                }
            except:
                # Couldn't parse spatial extra into bounding coordinates
                pass

        # ---- Reorganize resources by distributor, on/offline
        online = {}
        offline = {}
        for resource in p.get("resources", []):
            try:
                distributor = json.loads(resource.get("distributor", "{}"))
            except ValueError:
                # This will happen if the content of the distributor field is invalid JSON
                distributor = {}

            if json.loads(resource.get("is_online", "true")):
                resources = online
            else:
                resources = offline

            if distributor != {}:
                name = distributor.get("name", "None")
            else:
                name = "None"

            if name not in resources.keys():
                resources[name] = {
                    "distributor": distributor,
                    "resources": [resource]
                }
            else:
                resources[name]["resources"].append(resource)

        p["additional"]["online"] = [value for key, value in online.iteritems()]
        p["additional"]["offline"] = [value for key, value in offline.iteritems()]

        # ---- All done, render the template
        output = render_jinja2("package_to_iso.xml", p)

    return output