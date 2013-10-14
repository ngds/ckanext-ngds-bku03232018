__author__ = 'vivek'
from ckan.logic.schema import default_update_resource_schema, default_update_package_schema, default_create_package_schema
from ckan.lib.navl.validators import Invalid, not_empty, ignore_missing, not_missing, keep_extras, ignore
from ckan.logic.validators import extras_unicode_convert
from pylons.i18n import _
from ckanext.ngds.contentmodel.logic.action import contentmodel_checkFile


def ngds_resource_schema():
    resource_update_schema = default_update_resource_schema()
    resource_update_schema['resource_format'] = [valid_resource_type]
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
    if key not in data or data[key] == '':
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


def validate_content_model(key, data, errors, context):
    existence_check(key, data, errors, context)


def is_content_model_none(key, data, errors, context):
    if existence_check(key, data, errors, context) and data[key] == "None":
        return True


def is_content_model_version_none(key, data, errors, context):
    if not existence_check(key, data, errors, context):
        return True
    return False


def conforms_to_content_model(key, data, errors, context):
    if len(key) == 1:
        url_key = ('url',)
        cm_key = ('content_model_uri',)
        cmv_key = ('content_model_version',)
        err_key = ('content_model',)
    else:
        key_pre = key[0:2]
        url_key = key_pre + ('url',)
        cm_key = key_pre + ('content_model_uri',)
        cmv_key = key_pre + ('content_model_version',)
        err_key = key_pre + ('content_model',)

    url = data[url_key]
    cm = data[cm_key]
    cmv = data[cmv_key]
    split_version = cmv.split('/')
    cm_version = split_version[len(split_version) - 1]
    data_dict = {'cm_uri': cm, 'cm_version': cm_version, 'cm_resource_url': url}
    cm_validation_results = contentmodel_checkFile({}, data_dict)
    if not cm_validation_results['valid']:
        error_append(err_key, errors, cm_validation_results['messages'])


def validate_content_model_version(key, data, errors, context):
    existence_check(key, data, errors, context)


def validate_offline_resource_fields_present(key, data, errors, context):
    key_stub = key[0:2]
    ordering_procedure_key = key_stub + ('ordering_procedure',)
    validate_ordering_procedure(ordering_procedure_key, data, errors, context)


def validate_data_service_resource_fields_present(key, data, errors, context):
    key_stub = key[0:2]

    protocol_key = key_stub + ('protocol',)
    layer_key = key_stub + ('layer',)

    validate_distributor(key, data, errors, context)
    validate_protocol(protocol_key, data, errors, context)
    validate_layer(layer_key, data, errors, context)


def validate_structured_resource_fields_present(key, data, errors, context):
    key_stub = key[0:2]

    if key_stub[0] == 'resources':
        content_model_key = key_stub + ('content_model_uri',)
        content_model_version_key = key_stub + ('content_model_version',)
    else:
        content_model_key = ('content_model_uri',)
        content_model_version_key = ('content_model_version',)

    validate_content_model(content_model_key, data, errors, context)
    validate_distributor(key, data, errors, context)
    cm_none = is_content_model_none(content_model_key, data, errors, context)
    if cm_none:
        if is_content_model_version_none(content_model_version_key, data, errors, context):
            error_append(content_model_version_key, errors, _('Missing Value'))
        data.pop(content_model_key)
    else:
        cmv_none = is_content_model_version_none(content_model_version_key, data, errors, context)
        if not cm_none and not cmv_none:
            conforms_to_content_model(content_model_key, data, errors, context)


def validate_unstructured_resource_fields_present(key, data, errors, context):
    key_stub = key[0:2]
    validate_distributor(key, data, errors, context)


def validate_owner_org(key, data, errors, context):
    data[key] = "public"


def validate_extras(key, data, errors, context):
    if ("extras", 0, "key") not in data or data[("extras", 0, "value")] == "":
        errors[("authors",)] = [_("Missing value")]

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