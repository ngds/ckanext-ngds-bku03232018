import json
import os.path as path
import logging
import usginmodels
from ckanext.ngds.common import pylons_i18n as _
from ckanext.ngds.common import plugins as p
from ckanext.ngds.common import logic
from ckanext.ngds.common import config
from ckanext.ngds.common import storage

log = logging.getLogger(__name__)

def is_valid_json(key, data, errors, context):
    """
    Checks that a string can be parsed as JSON.

    @param key:
    @param data:
    @param errors:
    @param context:
    @return: None
    """

    try:
        json.loads(data[key])
    except:
        errors[key].append(_('Must be JSON serializable'))

def is_usgin_valid_data(key, data, errors, context):

    resource_id = data.get(('resources', 0, 'id'), None)
    resource_name = data.get(('resources', 0, 'name'), None)

    def get_file_path(res_id):
        dir_1 = res_id[0:3]
        dir_2 = res_id[3:6]
        file = res_id[6:]
        storage_base = config.get('ckan.storage_path', 'default')
        return path.join(storage_base, 'resources', dir_1, dir_2, file)

    validation_msg = []
    csv_file = get_file_path(resource_id)

    if csv_file is None:
        msg = p.toolkit._("Cannot find the full path of the resources from %s"\
            % resource_name)
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

    pass