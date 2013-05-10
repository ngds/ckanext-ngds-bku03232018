from nose.tools import ok_, eq_
import httplib
import ckan.model as model
import ckanext.importlib.spreadsheet_importer as spreadsheet_importer
import ckanext.ngds.lib.importer.validator as ngdsvalidator

import json
import ast

import requests
from nose.tools import *


# Use this method to initialize the database
def setUp(self):
    print ">>>>>>>>> Test Steup >>>>>>>>"
    assert True


# Use this method to reset the database
def teardown(self):
    print ">>>>>>>>>> Test Teardown >>>>>>>"
    assert True


def test_find_column_pos1():
    xl_file_path = "./testdata/test_find_pos.xls"
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>xl_file_path:",xl_file_path
    validator = ngdsvalidator.NGDSValidator(filepath=xl_file_path,resource_path=None,resource_list=None)

    validator.find_column_pos()

    #compare the expected column positions.
    print "self.mandatory_keys_pos: ",validator.mandatory_keys_pos
    print 'self.mandatory_keys_pos: %s date_field_pos: %s upload_file_pos: %s' % (validator.mandatory_keys_pos,validator.date_field_pos,validator.upload_file_pos)
    assert_equals(validator.mandatory_keys_pos,[(0,u'name'),(1,u'title')])
    assert_equals(validator.date_field_pos,[])
    assert_equals(validator.upload_file_pos,[(13, u'resource-0-upload_file')])

def test_find_column_pos2():
    xl_file_path = "./testdata/test_find_pos1.xls"
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>xl_file_path:",xl_file_path
    validator = ngdsvalidator.NGDSValidator(filepath=xl_file_path,resource_path=None,resource_list=None)

    validator.find_column_pos()

    print "self.mandatory_keys_pos: ",validator.mandatory_keys_pos
    print 'self.mandatory_keys_pos: %s date_field_pos: %s upload_file_pos: %s' % (validator.mandatory_keys_pos,validator.date_field_pos,validator.upload_file_pos)
    assert_equals(validator.mandatory_keys_pos,[(0,u'name'),(1,u'title')])
    assert_equals(validator.date_field_pos,[(8, u'publication_date')])
    assert_equals(validator.upload_file_pos,[(14, u'resource-0-upload_file')])

@raises(Exception)
def test_without_title_row():
    xl_file_path = "./testdata/without_title_row.xls"
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>xl_file_path:",xl_file_path
    validator = ngdsvalidator.NGDSValidator(filepath=xl_file_path,resource_path=None,resource_list=None)

    validator.find_column_pos()

    print "self.mandatory_keys_pos: ",validator.mandatory_keys_pos
    print 'self.mandatory_keys_pos: %s date_field_pos: %s upload_file_pos: %s' % (validator.mandatory_keys_pos,validator.date_field_pos,validator.upload_file_pos)
    assert_equals(validator.mandatory_keys_pos,[(0,u'name'),(1,u'title')])
    assert_equals(validator.date_field_pos,[(8, u'publication_date')])
    assert_equals(validator.upload_file_pos,[(14, u'resource-0-upload_file')])        

@raises(Exception)
def test_without_mandatory_fields():
    xl_file_path = "./testdata/without_mandatory.xls"
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>xl_file_path:",xl_file_path
    validator = ngdsvalidator.NGDSValidator(filepath=xl_file_path,resource_path=None,resource_list=None)

    validator.find_column_pos()
    validator._validate_mandatory_field()

@raises(Exception)
def test_invalid_date_fields():
    xl_file_path = "./testdata/invalid_date_fields.xls"
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>xl_file_path:",xl_file_path
    validator = ngdsvalidator.NGDSValidator(filepath=xl_file_path,resource_path=None,resource_list=None)

    validator.find_column_pos()
    try:
        validator._validate_date_field()    
    except Exception, e:
        print "exception: ",e
        assert False

   
''' 
    
def test_datastore_is_spatialized():
    assert True     
    

def test_datastore_is_exposed_as_layer():
    assert True


def test_datastore_expose_as_layer():
    
    api_key=_get_user_api_key()
    payload = {
    "resource_id": "e82f6b50-c7b4-42f9-ab24-0a1a2903557c",
    "col_geography": "shape",
    "col_longitude": "LONGITUDE", 
    "col_latitude": "LATITUDE"
    }
    
    url = 'http://localhost:5000/api/action/datastore_expose_as_layer'
    headers = {'Authorization': api_key,
               'X-CKAN-API-Key': api_key,
               'Content-Type':'application/json'}
    
    response = requests.post(url,data=json.dumps(payload),headers=headers)
    content = response.content
    content_dict = json.loads(content)
    result = content_dict["result"]
    
    print result
    assert result["success"] == True
    

def test_datastore_list_exposed_layers():
    
    api_key=_get_user_api_key()
    payload = {
    
    }
    
    url = 'http://localhost:5000/api/action/datastore_list_exposed_layers'
    headers = { 'Authorization': api_key,
                'X-CKAN-API-Key': api_key,
                'Content-Type':'application/json'}
    
    response = requests.post(url,data=json.dumps(payload),headers=headers)
    content = response.content
    print content
    
def test_datastore_remove_exposed_layer():
    
    api_key=_get_user_api_key()
    payload = {
       "layer_name": "e82f6b50-c7b4-42f9-ab24-0a1a2903557c"
    }
    
    url = 'http://localhost:5000/api/action/datastore_remove_exposed_layer'
    headers = { 'Authorization': api_key,
               'X-CKAN-API-Key': api_key,
               'Content-Type':'application/json'}
    
    response = requests.post(url,data=json.dumps(payload),headers=headers)
    content = response.content
    print content

def test_datastore_remove_all_exposed_layers():
    assert True
    
def test_geoserver_create_workspace():
    assert True
    
def test_geoserver_delete_workspace():
    assert True
    
def test_geoserver_create_store():
    assert True
    
def test_geoserver_delete_store():    
    assert True

#TODO: get this information from the real user, instead of hardcode it    
def _get_user_api_key():
    '''


   