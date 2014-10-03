import json
import os.path as path
import logging
import usginmodels
from ckanext.ngds.common import pylons_i18n
from ckanext.ngds.common import plugins as p
from ckanext.ngds.common import config
from ckanext.ngds.common import helpers as h
from ckanext.ngds.common import base
from ckanext.ngds.common import dictization_functions as df

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
        errors[key].append(pylons_i18n._('Must be JSON serializable'))

def is_usgin_valid_data(key, data, errors, context):
    Invalid = df.Invalid

    resource_id = data.get(('resources', 0, 'id'), None)

    if resource_id is None:
        return

    resource_name = data.get(('resources', 0, 'name'), None)

    ngds_resource = data.get(('extras',), None)
    ngds_resource = json.loads([i.get('value') for i in ngds_resource if \
                    i.get('key') == 'ngds_resource'][0])
    ngds_package = json.loads(data.get(('extras', 0, 'value'), None))

    uri = ngds_package.get('usginContentModel', None)
    version = ngds_package.get('usginContentModelVersion', None)
    layer = ngds_resource.get('usginContentModelLayer', None)

    def get_file_path(res_id):
        dir_1 = res_id[0:3]
        dir_2 = res_id[3:6]
        file = res_id[6:]
        storage_base = config.get('ckan.storage_path', 'default')
        return path.join(storage_base, 'resources', dir_1, dir_2, file)

    validation_msg = []
    csv_file = get_file_path(resource_id)

    if csv_file:
        log.info("Filename full path: %s " % csv_file)
    else:
        msg = base._("Cannot find the full path of the resources from %s"\
            % resource_name)
        validation_msg.append({
            'row': 0,
            'col': 0,
            'errorType': 'systemError',
            'message': msg
        })

    if 'none' in [uri.lower(), version.lower(), layer.lower()]:
        log.debug("Start USGIN content model validation")
        log.debug("USGIN tier 2 data model/version/layer are none")
        return {'valid': True}
    else:
        csv = open(csv_file, 'rbU')
        valid, errors, dataCorrected, long_fields, srs = \
            usginmodels.validate_file(csv, version, layer)

        log.debug("Finished USGIN content model validation")

        if valid and not errors:
            log.debug("USGIN document is valid")
        if valid and errors:
            log.debug('With changes the USGIN document will be valid')
            h.flash_error(base._('With changes the USGIN document will be valid'))
        else:
            log.debug('USGIN document is not valid')
            h.flash_error(base._('The USGIN document is not valid'))