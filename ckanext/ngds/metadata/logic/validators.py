import json
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

    pass