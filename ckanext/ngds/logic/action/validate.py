__author__ = 'kaffeine'
from ckan.logic.schema import default_update_resource_schema, default_update_package_schema
from ckan.lib.navl.validators import Invalid, not_empty, ignore_missing
from pylons.i18n import _


def ngds_resource_schema():
    resource_update_schema = default_update_resource_schema()
    resource_update_schema['resource_format'] = [valid_resource_type]
    resource_update_schema['ordering_procedure'] = [ignore_missing, validate_ordering_procedure]
    return resource_update_schema


def ngds_package_schema():
    package_update_schema = default_update_package_schema()
    package_update_schema['resources'] = ngds_resource_schema()
    return package_update_schema


def valid_resource_type(key, data, errors, context):
    resource_types = ("structured", 'unstructured', 'offline-resource', 'data-service')
    if "resource_format" in key and data[key] not in resource_types:
        raise Invalid(_(
            'Selecting a resource type is mandatory. Please select one of - Structured, Unstructured, Offline Resource or Data Service'))
    return data[key]


def resource_metadata_validator(key, data, errors, context):
    resource_format_key = key[0:2] + ('resource_format',)
    if resource_format_key not in data:
        raise Invalid(_(
            'Selecting a resource type is mandatory. Please select one of - Structured, Unstructured, Offline Resource or Data Service'))

    return data[key]


def validate_ordering_procedure(key, data, errors, context):
    if key not in data or data[key] == '':
        errors[key].append(_('Missing value'))
