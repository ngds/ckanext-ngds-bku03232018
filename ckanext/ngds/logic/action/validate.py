__author__ = 'vivek'
from ckan.logic.schema import default_update_resource_schema, default_update_package_schema, default_create_package_schema
from ckan.lib.navl.validators import Invalid, not_empty, ignore_missing
from pylons.i18n import _


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
    return package_update_schema


def default_package_schema():
    return default_create_package_schema()


def valid_resource_type(key, data, errors, context):
    resource_types = ("structured", 'unstructured', 'offline-resource', 'data-service')
    if "resource_format" in key and data[key] not in resource_types:
        raise Invalid(_(
            'Selecting a resource type is mandatory. Please select one of - Structured, Unstructured, Offline Resource or Data Service'))
    else:
        if data[key] == "offline-resource":
            validate_offline_resource_fields_present(key, data, errors, context)
        elif data[key] == 'data-service':
            validate_data_service_resource_fields_present(key, data, errors, context)
        elif data[key] == 'structured':
            validate_structured_resource_fields_present(key, data, errors, context)
    return data[key]


def resource_metadata_validator(key, data, errors, context):
    resource_format_key = key[0:2] + ('resource_format',)
    if resource_format_key not in data:
        raise Invalid(_(
            'Selecting a resource type is mandatory. Please select one of - Structured, Unstructured, Offline Resource or Data Service'))

    return data[key]


def existence_check(key, data, errors, context):
    if key not in data or data[key] == '':
        if key in errors:
            errors[key].append(_('Missing value'))
        else:
            errors[key] = []
            errors[key].append(_('Missing value'))
        return False
    return True


def validate_ordering_procedure(key, data, errors, context):
    existence_check(key, data, errors, context)


def validate_distributor(key, data, errors, context):
    existence_check(key, data, errors, context)


def validate_protocol(key, data, errors, context):
    existence_check(key, data, errors, context)


def validate_layer(key, data, errors, context):
    existence_check(key, data, errors, context)


def validate_content_model(key, data, errors, context):
    existence_check(key, data, errors, context)


def is_content_model_none(key, data, errors, context):
    if existence_check(key, data, errors, context) and data[key] == "none":
        return True


def validate_content_model_version(key, data, errors, context):
    existence_check(key, data, errors, context)


def validate_offline_resource_fields_present(key, data, errors, context):
    key_stub = key[0:2]
    ordering_procedure_key = key_stub + ('ordering_procedure',)
    validate_ordering_procedure(ordering_procedure_key, data, errors, context)


def validate_data_service_resource_fields_present(key, data, errors, context):
    key_stub = key[0:2]

    distributor_key = key_stub + ('distributor',)
    protocol_key = key_stub + ('protocol',)
    layer_key = key_stub + ('layer',)

    validate_distributor(distributor_key, data, errors, context)
    validate_protocol(protocol_key, data, errors, context)
    validate_layer(layer_key, data, errors, context)


def validate_structured_resource_fields_present(key, data, errors, context):
    key_stub = key[0:2]

    content_model_key = key_stub + ('content_model_uri',)
    content_model_version_key = key_stub + ('content_model_version',)

    validate_content_model(content_model_key, data, errors, context)
    cm_none = is_content_model_none(content_model_key, data, errors, context)
    if cm_none:
        data.pop(key)
    else:
        validate_content_model_version(content_model_version_key, data, errors, context)