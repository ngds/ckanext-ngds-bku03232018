
def validate_resource(context, data):
    if data['resource_type'] == 'offline-resource':
        return validate_offline_resource(context, data)
    if data['resource_type'] == 'data-service':
        return validate_data_service(context, data)
    if data['resource_type'] == 'unstructured':
        return validate_unstructured_resource(context, data)
    if data['resource_type'] == 'structured':
        return validate_structured_resource(context, data)


def validate_structured_resource(context, data):
    errors = []
    # A bunch of validations for the unstructured resource form

    from ckanext.ngds.contentmodel.logic.action import contentmodel_checkFile

    if not data['url'] or len(data['url']) < 3:
        errors.append({
            'field': 'url',
            'message': 'Resource URL is a mandatory parameter',
            'ref': 'form_validation'
        })

    if 'name' not in data or len(data['name']) == 0:
        errors.append({
            'field': 'name',
            'message': 'Name must be non-empty',
            'ref': 'form_validation'
        })
    url = data['url']

    cm_validation_results = {
        'valid': True
    }

    if 'content_model_uri' in data and 'url' in data and data['url'] != 'none' and data['url'] != '' and data['content_model_uri'] != 'none' and url[len(url)-3:len(url)] != 'zip':
        cm_uri = data['content_model_uri']
        cm_version = data['content_model_version']
        split_version = cm_version.split('/')
        cm_version = split_version[len(split_version)-1]
        data_dict = {'cm_uri': cm_uri, 'cm_version': cm_version, 'cm_resource_url': url}
        cm_validation_results = contentmodel_checkFile({}, data_dict)

    if cm_validation_results['valid'] == False:
        return {
            'success': False,
            'messages': cm_validation_results['messages'],
            'ref': 'content_model_validation_error',
            'display': 'Content Model Validation Errors'
        }

    if len(errors) > 0:
        return {
            'success': False,
            'display': 'Validation Errors',
            'type': 'resource_form_validation_error',
            'messages': errors
        }
    else:
        return {
            'success': True
        }

def validate_unstructured_resource(context, data):
    errors = []
    # A bunch of validations for the unstructured resource form

    if 'url' not in data or len(data['url']) < 3:
        errors.append({
            'field': 'url',
            'message': 'Resource URL is a mandatory parameter'
        })

    if 'name' not in data or len(data['name']) == 0:
        errors.append({
            'field': 'name',
            'message': 'Name must be non-empty'
        })

    if len(errors) > 0:
        return {
            'success': False,
            'display': 'Validation Errors',
            'type': 'resource_form_validation_error',
            'messages': errors
        }
    else:
        return {
            'success': True
        }


def validate_data_service(context, data):
    errors = []

    # A bunch of validations for the data service resource form
    if 'url' not in data or len(data['url']) < 3:
        errors.append({
            'field': 'url',
            'message': 'Resource URL is a mandatory parameter'
        })

    if 'name' not in data or len(data['name']) == 0:
        errors.append({
            'field': 'name',
            'message': 'Name must be non-empty'
        })

    if 'protocol' not in data or len(data['protocol']) == 0:
        errors.append({
            'field': 'protocol',
            'message': 'Protocol must be non-empty'
        })

    if 'layer' not in data or len(data['layer']) == 0:
        errors.append({
            'field': 'layer',
            'message': 'Layer must be non-empty'
        })

    if len(errors) > 0:
        return {
            'display': 'Validation Errors',
            'type': 'resource_form_validation_error',
            'messages': errors
        }
    else:
        return {
            'success': True
        }


def validate_offline_resource(context, data):
    errors = []

    # A bunch of validations for the offline resource form
    if 'name' not in data or len(data['name'])== 0:
        errors.append({
            'field': 'name',
            'message': 'Name must be non-empty'
        })

    if 'ordering_procedure' not in data or len(data['ordering_procedure']) == 0:
        errors.append({
            'field': 'ordering_procedure',
            'message': 'Ordering Procedure must be non-empty'
        })

    if len(errors) > 0:
        return {
            'display': 'Validation Errors',
            'type': 'resource_form_validation_error',
            'messages': errors
        }
    else:
        return {
            'success':True
        }