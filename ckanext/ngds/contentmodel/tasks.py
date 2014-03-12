__author__ = 'adrian'

import ckan.logic as logic
import usginmodels
from ContentModel_Utilities import *
from ckan.lib.celery_app import celery

@celery.task(name="contentmodel.usgin_validate")
def usgin_validate(data):

    log = logging.getLogger(__name__)
    _get_or_bust = logic.get_or_bust

    cm_resource_url = _get_or_bust(data, 'cm_resource_url')
    modified_resource_url = cm_resource_url.replace("%3A", ":")
    truncated_url = modified_resource_url.split("/storage/f/")[1]
    csv_filename_withfile = get_url_for_file(truncated_url)
    validation_msg = []

    if csv_filename_withfile is None:
        msg = toolkit._("Can't find the full path of the resources from %s" % cm_resource_url)
        validation_msg.append({'row':0, 'col':0, 'errorTYpe': 'systemError', 'message':msg})
    else:
        log.info("filename full path: %s " % csv_filename_withfile)

    this_layer = _get_or_bust(data, 'cm_layer')
    this_uri = _get_or_bust(data, 'cm_uri')
    this_version_uri = _get_or_bust(data, 'cm_version_url')

    if this_layer.lower() and this_uri.lower() and this_version_uri.lower() == 'none':
        log.debug("tier 2 data model/version/layer are none")
        data["usgin_valid"] = True
        data["usgin_errors"] = None
        return {"valid": True, "messages": "Okay"}
    else:
        log.debug("Starting USGIN content model validation")

        if len(validation_msg) == 0:
            try:
                csv_filename = csv_filename_withfile.split("file://")[1]
                this_csv = open(csv_filename, 'rbU')

                valid, errors, dataCorrected, long_fields, srs = usginmodels.validate_file(
                    this_csv,
                    this_version_uri,
                    this_layer
                )

                if errors and not valid:
                    validation_msg.append({'valid': False})
            except:
                validation_msg.append({'valid': False})

    if len(validation_msg) == 0:
        data["usgin_valid"] = True
        data["usgin_errors"] = None
        return {"valid": True, "messages": "Okay"}
    else:
        data["usgin_valid"] = False
        data["usgin_errors"] = validation_msg
        return {"valid": False, "messages": validation_msg}