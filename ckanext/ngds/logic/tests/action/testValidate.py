__author__ = 'Vivek'
import ckanext.ngds.logic.action.validate as validate_action

def test_validate_no_resource_format_provided():
    response = validate_action.validate_resource(None,{})
    assert response['success'] == False
    assert len(response['messages']) == 1
    assert response['messages'][0]['message'] == "Expecting parameter resource_format indicating the type of resource being validated. One of unstructured,structured,\
                          data-service,offline-resource"

def test_validate_empty_offline_resource():
    response = validate_action.validate_resource(None,{'resource_format':'offline-resource'})

    assert response['success'] == False
    assert len(response['messages']) == 2

    fields = get_fields(response)
    messages = get_messages(response)

    assert 'ordering_procedure' and 'name' in fields
    assert (len(message)>0 for message in messages)

def test_validate_offline_resource_no_ordering_procedure():
    response = validate_action.validate_resource(None,{'resource_format':'offline-resource','name':'an_offline_resource'})

    assert response['success'] == False
    assert len(response['messages']) == 1

    fields = get_fields(response)
    messages = get_messages(response)

    assert 'name' not in fields and 'ordering_procedure' in fields
    assert 'Ordering Procedure must be non-empty' in messages

def test_validate_offline_resource_no_name():
    response = validate_action.validate_resource(None,{'resource_format':'offline-resource','ordering_procedure':'This is the ordering procedure for this item'})

    assert response['success'] == False
    assert len(response['messages']) == 1

    fields = get_fields(response)
    messages = get_messages(response)

    assert 'name' in fields and 'ordering_procedure' not in fields
    assert 'Name must be non-empty' in messages

def test_validate_offline_resource_valid():
    response = validate_action.validate_resource(None,{'resource_format':'offline-resource','name':'a_name_for_this_resource','ordering_procedure':'This is the ordering procedure for this item'})

    assert response['success'] == True
    assert 'messages' not in response


def test_validate_data_service_empty():
    response = validate_action.validate_resource(None,{'resource_format':'data-service'})

    print response
    assert response['success'] == False

    fields = get_fields(response)
    messages = get_messages(response)

    assert set(['url','name','protocol','layer']).issuperset(fields)


def get_fields(wrapper):
    return set((item['field']) for item in wrapper['messages'])

def get_messages(wrapper):
    return set((item['message']) for item in wrapper['messages'])

test_validate_no_resource_format_provided()
test_validate_empty_offline_resource()
test_validate_offline_resource_no_ordering_procedure()
test_validate_offline_resource_no_name()
test_validate_offline_resource_valid()
test_validate_data_service_empty()