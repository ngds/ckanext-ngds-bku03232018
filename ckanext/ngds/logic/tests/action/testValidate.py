""" ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ """

from ckanext.ngds.logic.action import validators
from ckanext.ngds.logic.action.validate import validate_extras, validate_resources
import json

def test_apply_default_org():
    data = {"key": "something"}
    errors = {"key": []}
    validators.apply_default_org("key", data, errors, {})
    assert data["key"] == "public"

def test_is_valid_json():
    data = {"key": "not({ okay"}
    errors = {"key": []}
    validators.is_valid_json("key", data, errors, {})
    assert len(errors["key"]) == 1

    data = {"key": '{"this":"is fine"}'}
    errors = {"key": []}
    validators.is_valid_json("key", data, errors, {})
    assert len(errors["key"]) == 0

def test_is_valid_contact():
    data = {"key": '{"name":"Chuck", "email":"chunk@chub.com"}'}
    errors = {"key": []}
    validators.is_valid_contact("key", data, errors, {})
    assert len(errors["key"]) == 0

    data = {"key": '{"name":"Chuck"}'}
    errors = {"key": []}
    validators.is_valid_contact("key", data, errors, {})
    assert len(errors["key"]) == 1

def test_is_valid_list_of_contacts():
    data = {"key": '[{"name":"Chuck", "email":"chunk@chub.com"}]'}
    errors = {"key": []}
    validators.is_valid_list_of_contacts("key", data, errors, {})
    assert len(errors["key"]) == 0

    data = {"key": '{"name":"Chuck", "email":"chunk@chub.com"}'}
    errors = {"key": []}
    validators.is_valid_list_of_contacts("key", data, errors, {})
    assert len(errors["key"]) == 0
    assert isinstance(json.loads(data["key"]), list)

    data = {"key": '[{"name":"Chuck"}]'}
    errors = {"key": []}
    validators.is_valid_list_of_contacts("key", data, errors, {})
    assert len(errors["key"]) == 1

    data = {"key": '{"name":"Chuck"}'}
    errors = {"key": []}
    validators.is_valid_list_of_contacts("key", data, errors, {})
    assert len(errors["key"]) == 1
    assert isinstance(json.loads(data["key"]), list)

def test_is_valid_rectangle():
    geo = json.dumps({"type": "Polygon", "coordinates": [[
        [0,0], [1,0], [1,1], [0,1], [0,0]
    ]]})
    data = {"key": geo}
    errors = {"key": []}
    validators.is_valid_rectangle("key", data, errors, {})
    assert len(errors["key"]) == 0

    geo = json.dumps({"type": "Fake", "coordinates": [[
        [0,0], [1,0], [1,1], [0,1], [0,0]
    ]]})
    data = {"key": geo}
    errors = {"key": []}
    validators.is_valid_rectangle("key", data, errors, {})
    assert len(errors["key"]) == 1

    geo = json.dumps({"type": "Polygon", "coordinates": [[
        [0,0], [1,0], [1,1], [0,1]
    ]]})
    data = {"key": geo}
    errors = {"key": []}
    validators.is_valid_rectangle("key", data, errors, {})
    assert len(errors["key"]) == 1

    geo = json.dumps({"type": "Polygon", "coordinates": [[
        [0,0], [1,0], [1,1], [0,1], [0,3]
    ]]})
    data = {"key": geo}
    errors = {"key": []}
    validators.is_valid_rectangle("key", data, errors, {})
    assert len(errors["key"]) == 1

def test_is_in_list():
    valid = ["one", "two"]
    validation = validators.is_in_list(valid)
    data = {"key": "one"}
    errors = {"key": []}
    validation("key", data, errors, {})
    assert len(errors["key"]) == 0

    data = {"key": "pants"}
    validation("key", data, errors, {})
    assert len(errors["key"]) == 1

def test_is_valid_date():
    data = {"key": "2013-10-10T00:00:00"}
    errors = {"key": []}
    validators.is_valid_date("key", data, errors, {})
    assert len(errors["key"]) == 0

    data = {"key": "2013-10-10"}
    errors = {"key": []}
    validators.is_valid_date("key", data, errors, {})
    assert len(errors["key"]) == 0

    data = {"key": "03/04/2014"}
    errors = {"key": []}
    validators.is_valid_date("key", data, errors, {})
    assert len(errors["key"]) == 1

    data = {"key": None}
    errors = {"key": []}
    validators.is_valid_date("key", data, errors, {})
    assert len(errors["key"]) == 1

    data = {"key": ""}
    errors = {"key": []}
    validators.is_valid_date("key", data, errors, {})
    assert len(errors["key"]) == 1

def test_is_valid_model_uri():
    data = {"key": "http://schemas.usgin.org/uri-gin/ngds/dataschema/activefault/"}
    errors = {"key": []}
    validators.is_valid_model_uri("key", data, errors, {})
    assert len(errors["key"]) == 0

    data = {"key": "http://schemas.usgin.org/uri-gin/hambone/dataschema/activefault/"}
    errors = {"key": []}
    validators.is_valid_model_uri("key", data, errors, {})
    assert len(errors["key"]) == 1

def test_is_valid_model_version():
    data = {
        "content_model_uri": "http://schemas.usgin.org/uri-gin/ngds/dataschema/activefault/",
        "key": "1.1"
    }
    errors = {"key": []}
    validators.is_valid_model_version("key", data, errors, {})
    assert len(errors["key"]) == 0

    data = {
        "content_model_uri": "http://schemas.usgin.org/uri-gin/ngds/dataschema/activefault/",
        "key": "100.12"
    }
    errors = {"key": []}
    validators.is_valid_model_version("key", data, errors, {})
    assert len(errors["key"]) == 1

    data = {
        "content_model_uri": "http://faker",
        "key": "1.1"
    }
    errors = {"key": []}
    validators.is_valid_model_version("key", data, errors, {})
    assert len(errors["key"]) == 1

def test_check_uploaded_file():
    pass

def test_validate_extras():
    # Harder to test because these have real CKAN dependencies
    pass

def test_validate_resources():
    # Harder to test because these have real CKAN dependencies
    pass

test_apply_default_org()
test_is_valid_json()
test_is_valid_contact()
test_is_valid_list_of_contacts()
test_is_valid_rectangle()
test_is_in_list()
test_is_valid_date()
test_is_valid_model_uri()
test_is_valid_model_version()
test_check_uploaded_file()
test_validate_extras()
test_validate_resources()
