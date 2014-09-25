import json
import logging
from shapely.geometry import asShape
import usginmodels
from dateutil import parser as date_parser
from ckanext.ngds.common import plugins as p
from ckanext.ngds.common import logic
from ckanext.ngds.common import base
from ckanext.ngds.common import config
from ckanext.ngds.common import storage

log = logging.getLogger(__name__)

"""
Lifted from ckanext-ngds/ckanext/ngds/csw/logic/view.py
Kudos goes to Ryan Clark on this function and the template that it renders.  It takes any
CKAN package in JSON format and parses it into a dictionary object that can be passed into
a Jinja2 template to render an ISO XML metadata record of the package.
"""
@logic.side_effect_free
def iso_19139(context, data_dict):
    """
    Serialize a CKAN Package as an ISO 19139 XML document

    Gets the package to be converted, processes it, and passes it through a Jinja2 template
    which generates an XML string

    @param context: CKAN background noise
    @param data_dict: Must contain an "id" key which is a pointer to the package to serialize
    @return: ISO19139 XML string
    """

    pkg = logic.action.get.package_show(context, data_dict)

    # ---- Reformat extras so they can be looked up
    pkg["additional"] = {}
    for extra in pkg["extras"]:
        pkg["additional"][extra["key"]] = extra["value"]

    # ---- Remove milliseconds from metadata dates
    pkg["metadata_modified"] = date_parser.parse(pkg.get("metadata_modified", "")).replace(microsecond=0).isoformat()
    pkg["metadata_created"] = date_parser.parse(pkg.get("metadata_created", "")).replace(microsecond=0).isoformat()

    # ---- Make sure that there is a publication date (otherwise you'll get invalid metadata)
    if not pkg["additional"].get("publication_date", False):
        pkg["additional"]["publication_date"] = pkg["metadata_created"]

    # ---- Figure out URIs
    other_ids = pkg["additional"].get("other_id", "[]")
    if len(json.loads(other_ids)) > 0:
        pkg["additional"]["datasetUri"] = json.loads(other_ids)[0]
    else:
        pkg["additional"]["datasetUri"] = config.get("ckan.site_url", "http://default.ngds.com").rstrip("/") + \
            "/dataset/%s" % pkg["name"]

    # ---- Any other identifiers
    pkg['additional']['other_id'] = json.loads(pkg['additional'].get('other_id', '[]'))

    # ---- Load the authors
    authors = pkg["additional"].get("authors", None)
    try:
        pkg["additional"]["authors"] = json.loads(authors)
    except:
        pkg["additional"]["authors"] = [{"name": pkg["author"], "email": pkg["author_email"]}]

    # ---- Load Location keywords
    location = pkg["additional"].get("location", "[]")
    try:
        loc = json.loads(location)
        if not isinstance(loc, list):
            pkg["additional"]["location"] = [loc]
        else:
            pkg["additional"]["location"] = loc
    except:
        pkg["additional"]["location"] = []

    # ---- Reformat facets
    faceted_ones = [t for t in pkg.get("tags", []) if t.get("vocabulary_id") is not None]
    pkg["additional"]["facets"] = {}
    for faceted_tag in faceted_ones:
        vocab = p.toolkit.get_action("vocabulary_show")(None, {"id": faceted_tag.get("vocabulary_id", "")})
        vocab_name = vocab.get("name", None)
        if vocab_name is not None and vocab_name in pkg["additional"]["facets"]:
            pkg["additional"]["facets"][vocab_name].append(faceted_tag.get("display_name"))
        elif vocab_name is not None:
            pkg["additional"]["facets"][vocab_name] = [faceted_tag.get("display_name")]

    # ---- Extract BBOX coords from extras
    pkg["extent"] = {}

    geojson = pkg["additional"].get("spatial", None)

    if geojson is not None:
        try:
            bounds = asShape(json.loads(geojson)).bounds
            pkg["extent"] = {
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
    for resource in pkg.get("resources", []):
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

    pkg["additional"]["online"] = [value for key, value in online.iteritems()]
    pkg["additional"]["offline"] = [value for key, value in offline.iteritems()]

    # ---- All done, render the template
    output = base.render("xml/package_to_iso.xml", pkg)

    return output

@logic.side_effect_free
def usgin_validate(context, data_dict):

    def get_file_url(label):
        file_path = None
        try:
            ofs = storage.get_ofs()
            bucket = config.get('ckan.storage.bucket', 'default')
            file_path = ofs.get_url(bucket, label)
        except:
            pass
        return file_path

    validation_msg = []
    usgin_resource_url = logic.get_or_bust(data_dict, 'usgin_resource_url')
    mod_resource_url = usgin_resource_url.replace('%3A', ':')
    trunk_url = mod_resource_url.split('/storage/f/')[1]
    csv_file = get_file_url(trunk_url)

    if csv_file is None:
        msg = p.toolkit._("Cannot find the full path of the resources from %s"\
            % usgin_resource_url)
        validation_msg.append({
            'row': 0,
            'col': 0,
            'errorType': 'systemError',
            'message': msg
        })
    else:
        log.info("Filename full path: %s " % csv_file)

    layer = logic.get_or_bust(data_dict, 'usgin_layer')
    uri = logic.get_or_bust(data_dict, 'usgin_uri')
    version_uri = logic.get_or_bust(data_dict, 'version_uri')

    if layer.lower() and uri.lower() and version_uri.lower() == 'none':
        log.debug("USGIN tier 2 data model/version/layer are none")
        return {'valid': True}
    else:
        log.debug("Start USGIN content model validation")
        try:
            csv_filename = csv_file.split('file://')[1]
            csv = open(csv_filename, 'rbU')
            valid, errors, dataCorrected, long_fields, srs = \
                usginmodels.validate_file(csv, version_uri, layer)
            if errors: validation_msg.append({'valid': False})
        except:
            validation_msg.append({'valid': False})

        log.debug("Finished USGIN content model validation")
        if valid and not errors:
            log.debug("USGIN document is valid")
        if valid and errors:
            log.debug('With changes the USGIN document will be valid')
        else:
            log.debug('USGIN document is not valid')

    if len(validation_msg) == 0:
        return {'valid': True, 'usgin_errors': None}
    else:
        return {'valid': False, 'usgin_errors': validation_msg}