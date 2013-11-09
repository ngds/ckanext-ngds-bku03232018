''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

__author__ = 'vivek'
from ckan.logic.schema import default_update_resource_schema, default_update_package_schema, default_create_package_schema
from ckan.lib.navl.validators import Invalid, not_empty, ignore_missing, not_missing, keep_extras, ignore
from ckan.logic.validators import extras_unicode_convert
from pylons.i18n import _

from ckanext.ngds.contentmodel.logic.action import contentmodel_checkFile
from pylons import request
import json
from ckanext.ngds.contentmodel.logic.ContentModel_Utilities import get_url_for_file
from ckanext.ngds.logic.file_processors.FileProcessorFactory import FileProcessorFactory
import ckan.logic as logic


def ngds_resource_schema():
    resource_update_schema = default_update_resource_schema()
    resource_update_schema['resource_format'] = [not_missing, not_empty, valid_resource_type]
    resource_update_schema['ordering_procedure'] = [ignore_missing]
    resource_update_schema['distributor'] = [ignore_missing]
    resource_update_schema['format'] = [ignore_missing]
    resource_update_schema['protocol'] = [ignore_missing]
    resource_update_schema['layer'] = [ignore_missing]
    resource_update_schema['content_model_uri'] = [ignore_missing]
    resource_update_schema['content_model_version'] = [ignore_missing]

    return resource_update_schema


def ngds_package_schema():
    package_update_schema = default_update_package_schema()
    package_update_schema['resources'] = ngds_resource_schema()
    package_update_schema['owner_org'] = [validate_owner_org]
    package_update_schema['extras'] = {
        'id': [ignore],
        'key': [not_empty, unicode, validate_extras],
        'value': [not_missing],
        'state': [ignore],
        'deleted': [ignore_missing],
        'revision_timestamp': [ignore],
    }
    return package_update_schema


def default_package_schema():
    return default_create_package_schema()


def valid_resource_type(key, data, errors, context):
    resource_types = ("structured", 'unstructured', 'offline-resource', 'data-service')
    if "resource_format" not in key and data[key] not in resource_types:
        raise Invalid(_(
            'Selecting a resource type is mandatory. Please select one of - Structured, Unstructured, Offline Resource or Data Service'))
    else:
        if data[key] == "offline-resource":
            validate_offline_resource_fields_present(key, data, errors, context)
        elif data[key] == 'data-service':
            validate_data_service_resource_fields_present(key, data, errors, context)
        elif data[key] == 'structured':
            validate_structured_resource_fields_present(key, data, errors, context)
        elif data[key] == 'unstructured':
            validate_unstructured_resource_fields_present(key, data, errors, context)
    return data[key]


def resource_metadata_validator(key, data, errors, context):
    resource_format_key = key[0:2] + ('resource_format',)
    if resource_format_key not in data:
        raise Invalid(_(
            'Selecting a resource type is mandatory. Please select one of - Structured, Unstructured, Offline Resource or Data Service'))

    return data[key]


def error_append(key, errors, err):
    if key in errors:
        errors[key].append(err)
    else:
        errors[key] = []
        errors[key].append(err)


def existence_check(key, data, errors, context):
    if key not in data:
        error_append(key, errors, _('Missing value'))
        return False

    if data[key] == '':
        error_append(key, errors, _('Missing value'))
        return False

    return True


def validate_ordering_procedure(key, data, errors, context):
    existence_check(key, data, errors, context)


def validate_distributor(key, data, errors, context):
    if key[0] == 'resources':
        key_stub = key[0:2]
        distributor_key = key_stub + ('distributor',)
    else:
        distributor_key = ('distributor',)

    existence_check(distributor_key, data, errors, context)


def validate_protocol(key, data, errors, context):
    existence_check(key, data, errors, context)


def validate_layer(key, data, errors, context):
    existence_check(key, data, errors, context)


def is_content_model_none(key, data, errors, context):
    if not key in data:
        return True
    if data[key] == "None" or data[key] == "none":
        return True
    return False


def is_content_model_version_none(key, data, errors, context):
    if not existence_check(key, data, errors, context):
        return True
    return False


def line_count(key, data, errors, context, key_stub):
    if key not in data or data[key] == "":
        return

    url = data[key]
    if key_stub:
        lcount_key = key_stub + ('lcount', )
    else:
        lcount_key = ('lcount', )

    if not url.endswith('csv'):
        return

    try:
        modified_resource_url = url.replace("%3A", ":")
        truncated_url = modified_resource_url.split("/storage/f/")[1]
        filename_withfile = get_url_for_file(truncated_url)

        if filename_withfile:
            f = open(filename_withfile.split("file://")[1])
            count = len([line for line in f.readlines()])
            data[lcount_key] = count
            f.close()
    except Exception:
        return


def construct_key(key, field):
    if len(key) == 1:
        return (field,)
    return key[0:2] + (field, )


def conforms_to_content_model(key, data, errors, context):
    url_key = construct_key(key, 'url')
    cm_key = construct_key(key, 'content_model_uri')
    cmv_key = construct_key(key, 'content_model_version')
    err_key = construct_key(key, 'content_model')

    url = data[url_key]
    cm = data[cm_key]
    cmv = data[cmv_key]
    split_version = cmv.split('/')
    cm_version = split_version[len(split_version) - 1]
    data_dict = {'cm_uri': cm, 'cm_version': cm_version, 'cm_resource_url': url}

    if url != "":
        cm_validation_results = contentmodel_checkFile({}, data_dict)
        if not cm_validation_results['valid']:
            error_append(err_key, errors, cm_validation_results['messages'])
        else:
            fpf = FileProcessorFactory
            modified_resource_url = url.replace("%3A", ":")
            truncated_url = modified_resource_url.split("/storage/f/")[1]
            csv_filename_withfile = get_url_for_file(truncated_url).split("file://")[1]
            results = fpf.get_file_processor(csv_filename_withfile, cm, cmv, 'dummy_res_id').run_processes()
            for result in results:
                k = construct_key(key, result)
                data[k] = str(results[result])


def validate_content_model_version(key, data, errors, context):
    existence_check(key, data, errors, context)


def validate_offline_resource_fields_present(key, data, errors, context):
    key_stub = key[0:2]
    ordering_procedure_key = key_stub + ('ordering_procedure',)
    validate_ordering_procedure(ordering_procedure_key, data, errors, context)


def validate_data_service_resource_fields_present(key, data, errors, context):
    key_stub = key[0:2]

    if key_stub[0] == 'resources':
        distributor_key = key_stub + ('distributor',)
        protocol_key = key_stub + ('protocol',)
        layer_key = key_stub + ('layer',)
    else:
        distributor_key = ('distributor',)
        protocol_key = ('protocol',)
        layer_key = ('layer',)

    validate_distributor(distributor_key, data, errors, context)
    validate_protocol(protocol_key, data, errors, context)
    #validate_layer(layer_key, data, errors, context)


def validate_structured_resource_fields_present(key, data, errors, context):
    key_stub = key[0:2]

    if key_stub[0] == 'resources':
        content_model_key = key_stub + ('content_model_uri',)
        content_model_version_key = key_stub + ('content_model_version',)
        url_key = key_stub + ('url',)
        res_id_key = key_stub + ('id',)
        format_key = key_stub + ('format',)
        distributor_key = key_stub + ('distributor',)
    else:
        key_stub = None
        content_model_key = ('content_model_uri',)
        content_model_version_key = ('content_model_version',)
        url_key = ('url',)
        res_id_key = ('id',)
        format_key = ('format',)
        distributor_key = ('distributor',)

    line_count(url_key, data, errors, context, key_stub=key_stub)

    validate_distributor(distributor_key, data, errors, context)
    validate_format(format_key, data, errors, context)
    cm_none = is_content_model_none(content_model_key, data, errors, context)
    if cm_none:
        #if is_content_model_version_none(content_model_version_key, data, errors, context):
        #    error_append(content_model_version_key, errors, _('Missing Value'))
        if content_model_key in data:
            data.pop(content_model_key)
    else:
        cmv_none = is_content_model_version_none(content_model_version_key, data, errors, context)
        if not cm_none and not cmv_none:
            if has_resource_url_changed(res_id_key, url_key, data):
                conforms_to_content_model(content_model_key, data, errors, context)


def has_resource_url_changed(id_key, url_key, data):
    if not id_key in data:
        return True

    old_res = logic.get_action('resource_show')({}, {
                                                        'id': data[id_key]
                                                    })
    if not old_res['url'] == data[url_key]:
        return True

    return False


def validate_unstructured_resource_fields_present(key, data, errors, context):
    key_stub = key[0:2]
    if key_stub[0] == 'resources':
        format_key = key_stub + ('format',)
        distributor_key = key_stub + ('distributor',)
    else:
        format_key = ('format',)
        distributor_key = ('distributor',)

    validate_distributor(distributor_key, data, errors, context)
    validate_format(format_key, data, errors, context)


def validate_owner_org(key, data, errors, context):
    data[key] = "public"


def validate_format(key, data, errors, context):
    existence_check(key, data, errors, context)


def validate_extras(key, data, errors, context):
    if request.params.get('save') and request.params.get('save') == 'go-dataset':
        return

    if ("extras", 0, "key") not in data or data[("extras", 0, "value")] == "":
        errors[("authors",)] = [_("Missing value")]
    else:
        try:
            pattempt = json.loads(data[("extras", 0, "value")])
            if not isinstance(pattempt, list):
                data[("extras", 0, "value")] = "[" + data[("extras", 0, "value")] + "]"
        except Exception:
            data[("extras", 0, "value")] = "[" + data[("extras", 0, "value")] + "]"

    if ("extras", 1, "key") not in data or data[("extras", 1, "value")] == "":
        errors[("maintainer",)] = [_("Missing value")]

    if ("extras", 2, "key") not in data or data[("extras", 2, "value")] == "":
        errors[("spatial_word",)] = [_("Missing value")]

    if ("extras", 3, "key") not in data or data[("extras", 3, "value")] == "":
        errors[("dataset_category",)] = [_("Missing value")]

    if ("extras", 4, "key") not in data or data[("extras", 4, "value")] == "":
        errors[("dataset_uri",)] = [_("Missing value")]

    if ("extras", 5, "key") not in data or data[("extras", 5, "value")] == "":
        errors[("quality",)] = [_("Missing value")]

    if ("extras", 6, "key") not in data or data[("extras", 6, "value")] == "":
        errors[("lineage",)] = [_("Missing value")]

    if ("extras", 7, "key") not in data or data[("extras", 7, "value")] == "":
        errors[("status",)] = [_("Missing value")]

    if ("extras", 8, "key") not in data or data[("extras", 8, "value")] == "":
        errors[("publication_date",)] = [_("Missing value")]

    if ("extras", 9, "key") not in data or data[("extras", 9, "value")] == "":
        errors[("dataset_lang",)] = [_("Missing value")]

    if ("extras", 10, "key") not in data or data[("extras", 10, "value")] == "":
        errors[("spatial",)] = [_("Missing value")]