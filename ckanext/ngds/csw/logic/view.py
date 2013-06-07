from ckan.plugins import toolkit
from ckanext.harvest.model import HarvestObject
from shapely.geometry import asShape
import json

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
    harvest_object = context["model"].Session.query(HarvestObject) \
                    .filter(HarvestObject.package_id==p["id"]) \
                    .filter(HarvestObject.current==True) \
                    .first()
    # NOTE: If this is a harvested package, we should just return the XML, without alteration
    if harvest_object:
        output = harvest_object.content

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

        output = toolkit.render("package_to_iso.xml", p)

    return output