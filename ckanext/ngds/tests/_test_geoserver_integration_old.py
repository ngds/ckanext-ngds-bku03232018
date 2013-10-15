''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

from nose.tools import ok_, eq_
import httplib
import ckan.model as model
import pylons
import json
import ast

import requests
import time

from ckanclient import CkanClient
import ckanext.datastore.db as db

from unittest import TestCase

'''
Note that this test requires Celery deamon to be xecuting as well as ckan.
Ckan with NGDS extensions is expected on port 5000 of localhost
'''

class TestGeoserverIntegration (TestCase):
    
    millis = int(round(time.time() * 1000))
    package_name ='spatialize_test_resource_'+str(millis)
    id = "" # id of the resource used during testing
    
    # constructor of the class
    def __init__(self):
        print ">>>>>>>>> Constructor >>>>>>>"
        assert True

    # This method is called by nose before all tests are executed.
    # We use it to initialize the database
    def setUp(self):
        print ">>>>>>>>> Test Steup >>>>>>>>"
        self.id = self._setup_test_database(self.package_name)
        assert True
    
    
    # This method is called after all tests are executed
    # we use it to clean up the database
    def teardown(self):
        print ">>>>>>>>>> Test Teardown >>>>>>>"
        self._clean_test_database(self.package_name, self.id)
        assert True
    
    
    def test_datastore_spatialize(self):
        
        assert True
        
        
    def test_datastore_is_spatialized(self):
        assert True     
        
    
    # This method is not working properly so we made it private with an _
    # it is here just as an example on how to interact with the service
    # directly, i.e. via httplib
    def _test_datastore_expose_as_layer_old(self):
        
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
        hostname = self._get_hostname()
        port = self._get_port()
        action_uri = _get_action_uri()
        url = action_uri+'/datastore_expose_as_layer'
        api_key = self._get_user_api_key()
        resource_id =  self._get_resource_id()
        
        body =  '''{
            "resource_id": {0},
            "col_geography": "shape",
            "col_longitude": "LONGITUDE", 
            "col_latitude": "LATITUDE",
            'Authorization': api_key,
            'X-CKAN-API-Key': api_key
            }'''.format(resource_id)
        
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
    
    
    def test_datastore_is_exposed_as_layer(self):
        api_key = self._get_user_api_key()
        id = self._get_resource_id()
        payload = {
           "resource_id": id,
        }
        
        url = self._get_action_uri()+'/datastore_is_exposed_as_layer'
        headers = {'Authorization': api_key,
                   'X-CKAN-API-Key': api_key,
                   'Content-Type':'application/json'}
        
        response = requests.post(url,data=json.dumps(payload),headers=headers)
        content = response.content
        content_dict = json.loads(content)
        result = content_dict["result"]
        
        print result
        assert result["success"] == True
    
    
    def test_datastore_expose_as_layer(self):
        
        api_key=self._get_user_api_key()
        id = self._get_resource_id()
        payload = {
        "resource_id": id,
        "col_geography": "shape",
        "col_longitude": "LONGITUDE", 
        "col_latitude": "LATITUDE"
        }
        
        url = self._get_action_uri()+'/datastore_expose_as_layer'
        headers = {'Authorization': api_key,
                   'X-CKAN-API-Key': api_key,
                   'Content-Type':'application/json'}
        
        response = requests.post(url,data=json.dumps(payload),headers=headers)
        content = response.content
        content_dict = json.loads(content)
        result = content_dict["result"]
        
        print result
        assert result["success"] == True
        
    
    def test_datastore_list_exposed_layers(self):
        
        api_key=self._get_user_api_key()
        payload = {
        
        }
        
        url = self._get_action_uri()+'/datastore_list_exposed_layers'
        headers = { 'Authorization': api_key,
                    'X-CKAN-API-Key': api_key,
                    'Content-Type':'application/json'}
        
        response = requests.post(url,data=json.dumps(payload),headers=headers)
        content = response.content
        print content
        
    def test_datastore_remove_exposed_layer(self):
        
        api_key = self._get_user_api_key()
        layer_name = self._get_resource_id()
        
        payload = {
           "layer_name": layer_name
        }
        
        url = self._get_base_uri()+'/datastore_remove_exposed_layer'
        headers = { 'Authorization': api_key,
                   'X-CKAN-API-Key': api_key,
                   'Content-Type':'application/json'}
        
        response = requests.post(url,data=json.dumps(payload),headers=headers)
        content = response.content
        print content
    
    def test_datastore_remove_all_exposed_layers(self):
        assert True
        
    def test_geoserver_create_workspace(self):
        assert True
        
    def test_geoserver_delete_workspace(self):
        assert True
        
    def test_geoserver_create_store(self):
        assert True
        
    def test_geoserver_delete_store(self):    
        assert True
    
    #TODO: get this information from the real user, instead of hardcode it    
    def _get_user_api_key(self):
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
    
    def _get_ckan_base_api_url(self):
        #TODO: read this from the configuration file
        port = self._get_ckan_port()
        hostname = self._get_ckan_hostname()
        
        return "http://"+hostname+":"+port+"/api"
    
    def _get_action_uri(self):
        base_url = self._get_ckan_base_api_url()
        return base_url+"/action"
    
    def _get_ckan_port(self):
        return str(5000)
    
    def _get_ckan_hostname(self):
        return '127.0.0.1'
    
    def _get_resource_id(self):
        return self.id
   
    def _get_package_name(self):
        return self.package_name
    
    # this function restores the test database to its prestine state
    # this currently marks the record as deleted but it does not remove it from the databae.
    # a purse must be called in order to clean the database.
    def _clean_test_database(self, package_name, id):
        
        base_location = elf._get_ckan_base_api_url()
        api_key = self._get_user_api_key()
        testclient = CkanClient(base_location, api_key)
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
    def _setup_test_database(self, package_name):
        
        print ">>>>>>>>>>>>>>>>>> creating package: ",package_name
        try:
            base_location = self._get_ckan_base_api_url()
            api_key = self._get_user_api_key()
            testclient = CkanClient(base_location, api_key)
            file_url,status = testclient.upload_file("./testData/small_with_lat_long.csv")
        
            print "created file_url:",file_url
            
        except Exception, e:
            print "exception",e
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
        except Exception, e:
            print "exception",e
            assert False
        
        return database_id
    
         
'''
This gets executed if one runs this .py file by itself.
This file should be called with the nosetests command, so this will never execute.    
'''
if __name__ == '__main__':
    
    
   
    
    testObj = TestGeoserverIntegration()
    
    package_name = testObj._get_package_name()      
    id = testObj.setUp()
    
    testObj.test_datastore_expose_as_layer()
    testObj.test_datastore_is_exposed_as_layer()
    
    
    time.sleep(2) # wait for the database to be updated
    testObj.teardown()
    
    #test_datastore_expose_as_layer()
    #test_datastore_expose_as_layer()
    #test_datastore_list_exposed_layers()
    #test_datastore_remove_exposed_layer()
   
