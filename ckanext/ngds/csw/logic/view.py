from ckan.plugins import toolkit
from ckanext.harvest.model import HarvestObject
def iso_metadata(context, data_dict):
    """
    Serialize a CKAN Package as an ISO 19139 XML document

    Gets the package to be converted, processes it, and passes it through a Jinja2 template
    which generates an XML string

    @param context: CKAN background noise
    @param data_dict: Must contain an "id" key which is a pointer to the package to serialize
    @return: ISO19139 XML string
    """

    # NOTE: If this is a harvested package, we should just return the XML, straight up
    package_id = data_dict.get("id", "")
    p = toolkit.get_action("package_show")(context, {"id": package_id})

    # This is lifted from ckanext-harvest plugin.py:before_view. Looks for a HarvestObject to go with your package
    harvest_object = context["model"].Session.query(HarvestObject) \
                    .filter(HarvestObject.package_id==p["id"]) \
                    .filter(HarvestObject.current==True) \
                    .first()

    '''if harvest_object:
        output = harvest_object.content
    else:'''
    # Extract BBOX coords from extras
    bbox = {}

    def extract_coord(extra):
        bbox[extra["key"].split("-")[1]] = float(extra["value"])

    [extract_coord(e) for e in p["extras"] if e["key"].startswith("bbox-")]
    p["extent"] = bbox

    output = toolkit.render("package_to_iso.xml", p)

    return output