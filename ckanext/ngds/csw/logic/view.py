from ckan.plugins import toolkit
from ckanext.harvest.model import HarvestObject
from shapely.geometry import asShape
import json
from dateutil import parser as date_parser

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

    # This is lifted from ckanext-harvest plugin.py:before_view. Looks for a HarvestObject to go with your package
    '''harvest_object = context["model"].Session.query(HarvestObject) \
                    .filter(HarvestObject.package_id==p["id"]) \
                    .filter(HarvestObject.current==True) \
                    .first()'''
    harvest_object = None

    # NOTE: If this is a harvested package, we should just return the XML, without alteration
    if harvest_object:
        output = harvest_object.content

    else:
        # ---- Reformat extras so they can be looked up
        p["additional"] = {}
        for extra in p["extras"]:
            p["additional"][extra["key"]] = extra["value"]

        # ---- Remove milliseconds from metadata dates
        p["metadata_modified"] = date_parser.parse(p.get("metadata_modified", "")).replace(microsecond=0).isoformat()
        p["metadata_created"] = date_parser.parse(p.get("metadata_created", "")).replace(microsecond=0).isoformat()

        # ---- Figure out URIs
        other_ids = p["additional"].get("other_id", [])
        if len(other_ids) > 0:
            p["additional"]["datasetUri"] = other_ids[0]
        else:
            p["additional"]["datasetUri"] = "this should be the CKAN URL"

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

        # ---- Reformat resource extras
        for resource in p.get("resources", []):
            resource["additional"] = {}
            for e in resource.get("extras", []):
                resource["additional"][e["key"]] = e["value"]

        # ---- Reorganize resources by distributor, on/offline
        online = {}
        offline = {}
        for resource in p.get("resources", []):
            distributor = resource["additional"].get("distributor", None)

            if resource["additional"].get("is_online", True):
                resources = online
            else:
                resources = offline

            if distributor:
                name = distributor.get("distributor_name", "None")
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
        output = toolkit.render("package_to_iso.xml", p)

    return output