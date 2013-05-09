from nose.tools import ok_, eq_
import httplib
import ckan.model as model
import pylons
import json
import ast

import requests

from ckanclient import CkanClient
import ckanext.datastore.db as db

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

def _get_ckan_base_url():
    #TODO: read this from the configuration file
    return "http://localhost:5000/api"

# this function restores the test database to its prestine state
# this currently marks the record as deleted but it does not remove it from the databae.
# a purse must be called in order to clean the database.
def _clean_test_database(package_name, id):
    
    testclient = CkanClient(base_location=_get_ckan_base_url(), api_key=_get_user_api_key())
    #package_name ='spatialize_test_resource_3'
    testclient.package_entity_delete(package_name)
    
     
     #also remove table from database using id
    data_dict = {}
    data_dict['connection_url'] = pylons.config.get('ckan.datastore.write_url', 'postgresql://ckanuser:pass@localhost/datastore')  
    engine = db._get_engine(None, data_dict)
    connection = engine.connect()
    resources_sql = 'DROP TABLE IF EXISTS "'+id+'";'
    #resources_sql = 'DROP TABLE "b11351a2-5bbc-4f8f-8078-86a4eef1c7b0";'
    try:
        print '>>>>>>>>>>>>> Executing command: ',resources_sql
        results = connection.execute(resources_sql) 
    except Exception, e:
        print "exception",e
        assert False
# this function imports a resource to ckan. the resource will originate a
# databse in the postgress database
# in order for this to work, dont forget to run paster celeryd before using this function
def _setup_test_database(package_name):
    
    print ">>>>>>>>>>>>>>>>>> creating package: ",package_name
    try:
        testclient = CkanClient(base_location=_get_ckan_base_url(), api_key=_get_user_api_key())
        file_url,status = testclient.upload_file("./testData/small_with_lat_long.csv")
    
        print "created file_url:",file_url
        
    except:
        assert False   

    #construct package  and resource json object. set this file path in the resources.

    '''    
    package_dict = {u'name': package_name, u'title': u'Spatialize test resource 7', u'notes': u'dummy notes', 
    'owner_org': 'public', u'private': u'False', u'state': u'active', 'extras': {u'status': u'Completed', 
    u'spatial': u'{"type":"Polygon","coordinates":[[[-112.8515625,33.61461929233378],[-112.8515625,35.28150065789119],[-108.28125,35.28150065789119],[-108.28125,33.61461929233378],[-112.8515625,33.61461929233378]]]}'}, 
    'resources': [{'description': u'Resource Document Description','format': u'csv', 'url': file_url, 'name': u'Resouce in alaska3'}]}
    '''
    package_dict = {u'name': package_name, u'title': u'Spatialize test resource 7', u'notes': u'dummy notes', 
    'owner_org': 'public', u'private': u'False', u'state': u'active',   
    'resources': [{'description': u'Resource Document Description','format': u'csv', 'url': file_url, 'name': u'Resouce in alaska3'}]}
    
    print "package_dict: at test: ",package_dict
     
    try:
        ret_pack = testclient.package_register_post(package_dict)
        resources = ret_pack['resources']
        database_id = resources[0]['id'] 
    
        print ">>>>>>>>>>>>>>>>>>>>>>>> database_id:",database_id
    except:
        assert False
    
    return database_id
    
         
'''
This gets executed if one runs this .py file by itself.
This file should be called with the nosetests command, so this will never execute.    
'''
if __name__ == '__main__':
    
    import time
    millis = int(round(time.time() * 1000))
    
    package_name ='spatialize_test_resource_'+str(millis)       
    id = _setup_test_database(package_name)
    time.sleep(2)
    _clean_test_database(package_name, id)
    #test_datastore_expose_as_layer()
    #test_datastore_expose_as_layer()
    #test_datastore_list_exposed_layers()
    #test_datastore_remove_exposed_layer()
   