from ckan.plugins import toolkit
from ckanext.harvest.model import HarvestObject
from shapely.geometry import asShape
from pylons import config
import json

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
    if context is not None:
        harvested_content = get_harvested_content(package_id, context)

    if harvested_content:
        output = harvested_content

    else:
        # Extract BBOX coords from extras
        p["extent"] = {}

        # stupid python logic to try and get the first item or None from a list
        geojson = next(iter([k["value"] for k in p["extras"] if k["key"] == "spatial"]), None)

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

        output = render_jinja2("package_to_iso.xml", p)

    return output