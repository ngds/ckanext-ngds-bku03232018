from nose.tools import ok_, eq_
import httplib
import ckan.model as model

import json
import ast

import requests


# Use this method to initialize the database
def setUp(self):
    print ">>>>>>>>> Test Steup >>>>>>>>"
    assert True


# Use this method to reset the database
def teardown(self):
    print ">>>>>>>>>> Test Teardown >>>>>>>"
    assert True


def test_datastore_spatialize():
    assert True
    
    
def test_datastore_is_spatialized():
    assert True     
    

# This method is not working properly so we made it private with an _
# it is here just as an example on how to interact with the service
# directly, i.e. via httplib
def _test_datastore_expose_as_layer():
    
    '''
    sys_user = model.User.get('admin')
    
    sysadmin_user = {
       'id': sys_user.id,
       'apikey': sys_user.apikey,
       'name': sys_user.name,
       }
    '''
    print ">>>>>>>>>>>>>>>>> sending create layer POST >>>>>>>>>>>>>>>>"
    
    #headers, response = cat.http.request(featureType_url, "POST", definition.serialize(), headers)
    hostname = '127.0.0.1'
    port = 5000
    url = '/api/action/datastore_expose_as_layer'
    api_key = _get_user_api_key()
    body =  '''{
    "resource_id": "e82f6b50-c7b4-42f9-ab24-0a1a2903557c",
    "col_geography": "shape",
    "col_longitude": "LONGITUDE", 
    "col_latitude": "LATITUDE",
    'Authorization': api_key,
    'X-CKAN-API-Key': api_key
    }'''
    
    json_body = json.dumps(body)
    
    method = "POST"
    headers = {"Content-type": "text/xml"}

    httpServ = httplib.HTTPConnection(hostname, port)
    httpServ.connect()
    httpServ.request(method, url, body, headers)
    
    print ">>>>>>>>>>>>>>>>> getting response >>>>>>>>>>>>>>>>"
    response = httpServ.getresponse()
    print response
    if response.status == httplib.OK:
        assert True
    else:
        assert False
    print " Output from HTTP request:"
    print response.read()
        
    httpServ.close()


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
    sys_user = model.User.get('admin')
    
    print "sys_user: ",sys_user
    
    sysadmin_user = {
       'id': sys_user.id,
       'apikey': sys_user.apikey,
       'name': sys_user.name,
    }
    
    print sysadmin_user
    '''
    # this is hardcoded now.
    return  '6397972f-fd52-456b-a6ee-cc4c6a4d7fdb'
         
'''
This gets executed if one runs this .py file by itself.
This file should be called with the nosetests command, so this will never execute.    
'''
if __name__ == '__main__':
   #test_datastore_expose_as_layer()
   test_datastore_expose_as_layer()
   #test_datastore_list_exposed_layers()
   #test_datastore_remove_exposed_layer()
   