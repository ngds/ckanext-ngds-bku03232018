from inspect import isfunction
from ckanext.ngds.metadata.model.additional_metadata import ResponsibleParty
import ast
from ckan.model import meta
from ckanext.ngds.contentmodel.logic.action import contentmodel_checkFile
from ckan.plugins import toolkit


def validate_dataset_metadata(context, data):
    '''
    This function is the main entry point to validating a dataset's metadata.
    :param context:
    :param data:
    :return:
    '''
    errors = {}
    check_existence(data, errors)

    if len(errors) > 0:


        return {
            "success": False,
            'errors': errors,
            'data': data
        }
    else:
        return {
            "success": True
        }


def validate_resource(context, data):
    '''
    The main entry point to validating a resource.
    :param context:
    :param data:
    :return:
    '''
    if 'resource_format' not in data:
        return {
            'success': False,
            'display': 'Parameter error',
            'messages': [
                {'message': "Expecting parameter resource_format indicating the type of resource being validated. One of unstructured,structured,\
                          data-service,offline-resource"}
            ]
        }

    if data['resource_format'] == 'offline-resource':
        return validate_offline_resource(data)
    if data['resource_format'] == 'data-service':
        return validate_data_service(data)
    if data['resource_format'] == 'unstructured':
        return validate_unstructured_resource(data)
    if data['resource_format'] == 'structured':
        return validate_structured_resource(data)


def validate_structured_resource(data):
    errors = []
    # A bunch of validations for the unstructured resource form

    if not data['url'] or len(data['url']) < 3:
        errors.append({
            'field': 'url',
            'message': toolkit._('Resource URL is a mandatory parameter'),
            'ref': 'form_validation'
        })

    if 'name' not in data or len(data['name']) == 0:
        errors.append({
            'field': 'name',
            'message': toolkit._('Name must be non-empty'),
            'ref': 'form_validation'
        })
    url = data['url']

    cm_validation_results = {
        'valid': True
    }

    if 'content_model_uri' in data and 'url' in data and data['url'] != 'none' and data['url'] != '' and data[
        'content_model_uri'] != 'none' and url[len(url) - 3:len(url)] != 'zip':
        cm_uri = data['content_model_uri']
        cm_version = data['content_model_version']
        split_version = cm_version.split('/')
        cm_version = split_version[len(split_version) - 1]
        data_dict = {'cm_uri': cm_uri, 'cm_version': cm_version, 'cm_resource_url': url}
        cm_validation_results = contentmodel_checkFile({}, data_dict)

    if cm_validation_results['valid'] == False:
        return {
            'success': False,
            'messages': cm_validation_results['messages'],
            'ref': 'content_model_validation_error',
            'display': toolkit._('Content Model Validation Errors')
        }

    if len(errors) > 0:
        return {
            'success': False,
            'display': toolkit._('Validation Errors'),
            'type': 'resource_form_validation_error',
            'messages': errors
        }
    else:
        return {
            'success': True
        }


def validate_unstructured_resource(data):
    errors = []
    # A bunch of validations for the unstructured resource form

    if 'url' not in data or len(data['url']) < 3:
        errors.append({
            'field': 'url',
            'message': toolkit._('Resource URL is a mandatory parameter')
        })

    if 'name' not in data or len(data['name']) == 0:
        errors.append({
            'field': 'name',
            'message': toolkit._('Name must be non-empty')
        })

    if len(errors) > 0:
        return {
            'success': False,
            'display': toolkit._('Validation Errors'),
            'type': 'resource_form_validation_error',
            'messages': errors
        }
    else:
        return {
            'success': True
        }


def validate_data_service(data):
    errors = []

    # A bunch of validations for the data service resource form
    if 'url' not in data or len(data['url']) < 3:
        errors.append({
            'field': 'url',
            'message': toolkit._('Resource URL is a mandatory parameter')
        })

    if 'name' not in data or len(data['name']) == 0:
        errors.append({
            'field': 'name',
            'message': toolkit._('Name must be non-empty')
        })

    if 'protocol' not in data or len(data['protocol']) == 0:
        errors.append({
            'field': 'protocol',
            'message': toolkit._('Protocol must be non-empty')
        })

    if 'layer' not in data or len(data['layer']) == 0:
        errors.append({
            'field': 'layer',
            'message': toolkit._('Layer must be non-empty')
        })

    if len(errors) > 0:
        return {
            'display': toolkit._('Validation Errors'),
            'type': 'resource_form_validation_error',
            'success': False,
            'messages': errors
        }
    else:
        return {
            'success': True
        }


def validate_offline_resource(data):
    errors = []

    # A bunch of validations for the offline resource form
    if 'name' not in data or len(data['name']) == 0:
        errors.append({
            'field': 'name',
            'message': toolkit._('Name must be non-empty')
        })

    if 'ordering_procedure' not in data or len(data['ordering_procedure']) == 0:
        errors.append({
            'field': 'ordering_procedure',
            'message': toolkit._('Ordering Procedure must be non-empty')
        })

    if len(errors) > 0:
        return {
            'display': toolkit._('Validation Errors'),
            'type': 'resource_form_validation_error',
            'success': False,
            'messages': errors
        }
    else:
        return {
            'success': True
        }


def check_existence(data, collector):
    if not "extras" in data:
        collector["extras"] = toolkit._("No extras specified")
        if 'spatial' in data['extras']:
            if data['extras']['spatial'] == "" or data['extras']['spatial'] == None or data['extras'][
                'spatial'] == "null":
                del data['extras']['spatial']
        return collector

    if not is_valid_maintainer(data):
        collector['maintainer'] = toolkit._("Maintainer must be specified")

    if not valid_extra("uri", data['extras'], lambdafn=lambda val: len(val) > 4):
        collector['uri'] = toolkit._("URI must be specified")

    if not valid_extra("status", data['extras'], lambdafn=lambda val: val in ["Completed", "Ongoing", "Deprecated"]):
        collector['status'] = toolkit._("Status must be specified")

    if not is_valid_authors_list(data):
        collector['authors'] = toolkit._("At least one author must be specified")

    return collector


def get_extra(key, extras):
    for item in extras:
        if item['key'] == key:
            return item
    return None


def valid_extra(key, extras, lambdafn):
    extra = get_extra(key, extras)

    if extra == None or extra["value"] == "" or extra["value"] == None:
        return False

    if isfunction(lambdafn):
        return lambdafn(extra['value'])

    return True


def is_valid_maintainer(payload):
    return (("maintainer" and "maintainer_email" in payload) \
                and valid_extra("ngds_maintainer", payload["extras"],
                                lambdafn=lambda val: isinstance(ast.literal_eval(val), dict)) \
                and payload["maintainer_email"] ==
            ast.literal_eval(get_extra("ngds_maintainer", payload["extras"])["value"])["email"] \
                and payload["maintainer"] == ast.literal_eval(get_extra("ngds_maintainer", payload["extras"])["value"])[
                "name"] \
                and responsible_party_exists(payload["maintainer_email"]))


def is_valid_authors_list(payload):
    if valid_extra("authors", payload["extras"], lambdafn=lambda val: isinstance(ast.literal_eval(val), list)):
        authors = ast.literal_eval(get_extra("authors", payload["extras"])["value"])
        for author in authors:
            if not responsible_party_exists(author["email"]):
                return False
        return True
    return False


def responsible_party_exists(email):
    try:
        responsible_party = meta.Session.query(ResponsibleParty).filter(ResponsibleParty.email == email)
        if responsible_party.first().email == email:
            return True
    except Exception as e:
        pass
        # swallow it
    return False