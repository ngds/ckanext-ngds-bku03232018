""" NGDS_HEADER_BEGIN

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey

Please refer the the README.txt file in the base directory of the NGDS project:
https://github.com/ngds/ckanext-ngds/blob/master/README.txt

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero
General Public License as published by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.  https://github.com/ngds/ckanext-ngds
ngds/blob/master/LICENSE.md or
http://www.gnu.org/licenses/agpl.html

NGDS_HEADER_END """

#from nose.tools import ok_, eq_

import unittest
import httplib
import ckan.model as model
import pylons
import json
import ast

import requests
import time

from pylons import config

from ckanclient import CkanClient
import ckanext.datastore.db as db



'''
Note that this test requires Celery deamon to be executing as well as ckan.
Ckan with NGDS extensions is expected on port 5000 of localhost
'''

class TestGeoserverIntegration (unittest.TestCase):
    
    millis = int(round(time.time() * 1000))
    package_name = 'spatialize_test_resource_' + str(millis)
    id = ""  # id of the resource used during testing
    engine = None

# ============================== Fixtures ===============================
    
    # constructor of the class
    
    
    def __init__(self, test = None, config=None, resultProxy=None):
        print ">>>>>>>>> Constructor >>>>>>>"
        assert True
    
    
    # This method is called by nose before all test_ methods are called in 
    # instances of this object.
    # We use it to initialize the database
    def setUp(self):
        print ">>>>>>>>> Test Setup >>>>>>>>"
        self.id = self._setup_test_database(self.package_name)
        time.sleep(2)  # wait for the data to be stored in the database through celeryd
        assert True
    
    
    # This method is called after all test* methods are executed in instances of
    # this class.
    # we use it to clean up the database
    def teardown(self):
        print ">>>>>>>>>> Test Teardown >>>>>>>"
        # time.sleep(1) # wait for the database to be updated
        self._clean_test_database(self.package_name, self.id)
        assert True
 
 # =========================== Test methods ===============================   
    
    '''
    Spatialization does everything: it not only spatializes the database table
    but also publishes it as a layer in geoserver. This is the most complete test.
    '''
    def test_datastore_spatialize_scenario(self):
        
        print ">>>>>>>>> The resource is not spatialized yet >>>>>>>>>"
        result0 = self._REST_datastore_is_spatialized()
        assert result0 == False
        
        print ">>>>>>>>> No layer should be exposed >>>>>>>>>"
        result1 = self._REST_datastore_is_exposed_as_layer()
        assert result1 == False
        
        print ">>>>>>>>> Spatializing >>>>>>>>>"
        result2 = self._REST_datastore_spatialize()
        assert result2 == True
    
        print ">>>>>>>>> verifying spatialization >>>>>>>>>"
        result3 = self._REST_datastore_is_spatialized()
        assert result3 == True

        print ">>>>>>>>> Verifying exposing as layer >>>>>>>>>"
        result4 = self._REST_datastore_is_exposed_as_layer()
        assert result4 == True    
        
    
    # Expose as layer is actually called within spatialize function, so we 
    # do not to test for it explicitly here.
    '''
    def test_datastore_expose_as_layer_scnario(self):
        print ">>>>>>>>> No layer should be exposed >>>>>>>>>"
        result0 = self._REST_datastore_is_exposed_as_layer()
        assert result0 == False
        
        print ">>>>>>>>> Exposing as layer >>>>>>>>>"
        result = self._REST_datastore_expose_as_layer()
        assert result == True
        
        print ">>>>>>>>> Verifying exposing as layer >>>>>>>>>"
        result2 = self._REST_datastore_is_exposed_as_layer()
        assert result2 == True
        
        result3 = self._REST_datastore_list_exposed_layers()
        print "Exposed layers: "
        print result3
   
    '''
    # After testing the spatialization functions, we test the
    # functions that remove the layer from the server                       
    def test_datastore_remove_exposed_layer(self):
        print ">>>>>>>>> The resource is spatialized >>>>>>>>>"
        result0 = self._REST_datastore_is_spatialized()
        assert result0 == True
        
        print ">>>>>>>>> Layer should be exposed >>>>>>>>>"
        result1 = self._REST_datastore_is_exposed_as_layer()
        assert result1 == True
        
        print ">>>>>>>>> Removing layer >>>>>>>>>"
        result = self._REST_datastore_remove_exposed_layer()
        assert result == True
        
        print ">>>>>>>>> No layer should be exposed >>>>>>>>>"
        result2 = self._REST_datastore_is_exposed_as_layer()
        assert result2 == False
        
    
    # This test case not only removes the single resource we
    # published in the former two tests, but also removes any other
    # resource exposed thorugh the spatialize function in the specific
    # database    
    def test_datastore_remove_all_exposed_layers(self):
        
        print ">>>>>>>>> List all exposed layers >>>>>>>>>"
        response = self._REST_datastore_list_exposed_layers()
        result = response["result"]
        assert result["success"] == True
        assert len(result["list_of_layers"]) > 0
        
        print ">>>>>>>>> Removing all exposed layers >>>>>>>>>"
        result = self._REST_datastore_remove_all_exposed_layers()
        assert result == True
        
    
    # This test case verifies the basic functions used to create and
    # delete workspaces and stores    
    def test_workspace_and_store_management_functions(self):
        # create, list, delete workspace
        print ">>>>>>>>> Creating test workspace >>>>>>>>>"
        result = self._REST_geoserver_create_workspace()
        assert result == True
        
        print ">>>>>>>>> Creating test store >>>>>>>>>"
        result = self._REST_geoserver_create_store()
        assert result == True
        
        print ">>>>>>>>> Creating test store >>>>>>>>>"
        result = self._REST_geoserver_delete_store()
        assert result == True
        
        print ">>>>>>>>> Deleting test workspace >>>>>>>>>"
        result = self._REST_geoserver_delete_workspace()
        assert result == True
         
    
# ================================ Auxiliary functions ===============================    
    
    def _REST_geoserver_delete_store(self):
        api_key = self._get_user_api_key()
        id = self._get_resource_id()
        
        store_name  = 'test_datastore'   
        workspace_name = 'test_workspace'     
        
        payload = {
            'workspace_name': workspace_name,
            'store_name': store_name
        }
        
        url = self._get_action_uri() + '/geoserver_delete_store'
        print ">>>>>>>>>>>>>> Action URL: ", url
        #print ">>>>>>>>>>>>>> Payload: ", json.dumps(payload)
        
        headers = {'Authorization': api_key,
                   'X-CKAN-API-Key': api_key,
                   'Content-Type':'application/json'}
        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        content = response.content
        #print ">>>>>>>>>>>>>>>>>> Content: ", content
        content_dict = json.loads(content)
        result = content_dict["result"]
        
        #print result
        return bool(result["success"])

    def _REST_geoserver_create_store(self):
        api_key = self._get_user_api_key()
        id = self._get_resource_id()
        
        config_login      = 'ckanuser'
        config_passwd     = 'pass'
        config_datastore  = 'test_datastore'
        
        # reads geoserver information from development.ini file or returns a default value
        geoserver_rest_url = pylons.config.get('ckan.geoserver.rest_url', 'http://localhost:8080/geoserver/rest')    
            
        # we utilize default values, instead of failing, if those parameters are not provided 
        geoserver = geoserver_rest_url
        store_name = config_datastore
        pg_host = 'localhost'
        pg_port = '5432'
        pg_db = config_datastore
        pg_user = config_login
        pg_password = config_passwd
        db_type = 'postgis'
        workspace_name = 'test_workspace'     
        
        payload = {
            'geoserver': geoserver,
            'workspace_name': workspace_name,
            'store_name': store_name,
            'pg_host': pg_host,
            'pg_port': pg_port,
            'pg_db' : pg_db,
            'pg_user' : pg_user,
            'pg_password': pg_password,
            'db_type' : db_type
        }
        
        url = self._get_action_uri() + '/geoserver_create_store'
        print ">>>>>>>>>>>>>> Action URL: ", url
        #print ">>>>>>>>>>>>>> Payload: ", json.dumps(payload)
        
        headers = {'Authorization': api_key,
                   'X-CKAN-API-Key': api_key,
                   'Content-Type':'application/json'}
        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        content = response.content
        #print ">>>>>>>>>>>>>>>>>> Content: ", content
        content_dict = json.loads(content)
        result = content_dict["result"]
        
        print result
        return bool(result["success"])
    
    def _REST_geoserver_create_workspace(self):
        api_key = self._get_user_api_key()
        id = self._get_resource_id()
        
        workspace_name = "test_workspace"
        workspace_uri = 'http://localhost:5000/test_workspace'
        
        payload = {
            "workspace_name": workspace_name,
            "workspace_uri": workspace_uri
        }
        
        url = self._get_action_uri() + '/geoserver_create_workspace'
        print ">>>>>>>>>>>>>> Action URL: ", url
        #print ">>>>>>>>>>>>>> Payload: ", json.dumps(payload)
        
        headers = {'Authorization': api_key,
                   'X-CKAN-API-Key': api_key,
                   'Content-Type':'application/json'}
        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        content = response.content
        #print ">>>>>>>>>>>>>>>>>> Content: ", content
        content_dict = json.loads(content)
        result = content_dict["result"]
        
        #print result
        return bool(result["success"])
    
    
    def _REST_geoserver_delete_workspace(self):
        api_key = self._get_user_api_key()
        id = self._get_resource_id()
        
        workspace_name = "test_workspace"
        
        # reads geoserver information from development.ini file or returns a default value
        geoserver_rest_url = pylons.config.get('ckan.geoserver.rest_url', 'http://localhost:8080/geoserver/rest')    
        
        
        payload = {
            "workspace_name": workspace_name,
            "geoserver": geoserver_rest_url
        }
        
        url = self._get_action_uri() + '/geoserver_delete_workspace'
        print ">>>>>>>>>>>>>> Action URL: ", url
        #print ">>>>>>>>>>>>>> Payload: ", json.dumps(payload)
        
        headers = {'Authorization': api_key,
                   'X-CKAN-API-Key': api_key,
                   'Content-Type':'application/json'}
        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        content = response.content
        #print ">>>>>>>>>>>>>>>>>> Content: ", content
        content_dict = json.loads(content)
        result = content_dict["result"]
        
        #print result
        return bool(result["success"])
    
    
    
    def _REST_datastore_spatialize(self):
        api_key = self._get_user_api_key()
        id = self._get_resource_id()
        payload = {
            "resource_id": id,
            "col_geography": "shape",
            "col_longitude": "LONGITUDE",
            "col_latitude": "LATITUDE"
        }
        
        url = self._get_action_uri() + '/datastore_spatialize'
        print ">>>>>>>>>>>>>> Action URL: ", url
        #print ">>>>>>>>>>>>>> Payload: ", json.dumps(payload)
        
        headers = {'Authorization': api_key,
                   'X-CKAN-API-Key': api_key,
                   'Content-Type':'application/json'}
        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        content = response.content
        #print ">>>>>>>>>>>>>>>>>> Content: ", content
        content_dict = json.loads(content)
        result = content_dict["result"]
        
        #print result
        return bool(result["success"])
    
        
    def _REST_datastore_is_spatialized(self):
        api_key = self._get_user_api_key()
        id = self._get_resource_id()
        payload = {
           "resource_id": id,
           "col_geography": "shape"
        }
        
        url = self._get_action_uri() + '/datastore_is_spatialized'
        headers = {'Authorization': api_key,
                   'X-CKAN-API-Key': api_key,
                   'Content-Type':'application/json'}
        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        content = response.content
        content_dict = json.loads(content)
        
        if content_dict["success"] == True:
            result = content_dict["result"]
            return bool(result["is_spatialized"])
        else:
            return False  
    
    def _REST_datastore_is_exposed_as_layer(self):
        api_key = self._get_user_api_key()
        id = self._get_resource_id()
        payload = {
           "resource_id": id
        }
        
        url = self._get_action_uri() + '/datastore_is_exposed_as_layer'
        headers = {'Authorization': api_key,
                   'X-CKAN-API-Key': api_key,
                   'Content-Type':'application/json'}
        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        content = response.content
        content_dict = json.loads(content)
        result = content_dict["result"]
        
        #print "Result: ", result
        return bool(result["is_exposed_as_layer"])
    
    
    def _REST_datastore_expose_as_layer(self):
        
        api_key = self._get_user_api_key()
        id = self._get_resource_id()
        
        payload = {
            "resource_id": id
        }
        
        '''
        payload = {
        "resource_id": id,
        "col_geography": "shape",
        "col_longitude": "LONGITUDE", 
        "col_latitude": "LATITUDE"
        }
        '''
        
        url = self._get_action_uri() + '/datastore_expose_as_layer'
        headers = {'Authorization': api_key,
                   'X-CKAN-API-Key': api_key,
                   'Content-Type':'application/json'}
        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        content = response.content
        content_dict = json.loads(content)
        result = content_dict["result"]
        
        #print result
        return bool(result["success"])
        
    
    def _REST_datastore_list_exposed_layers(self):
        
        api_key = self._get_user_api_key()
        payload = {
        
        }
        
        url = self._get_action_uri() + '/datastore_list_exposed_layers'
        headers = { 'Authorization': api_key,
                    'X-CKAN-API-Key': api_key,
                    'Content-Type':'application/json'}
        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        content = json.loads(response.content)
        
        #print content
        return content
        
    def _REST_datastore_remove_exposed_layer(self):
        
        api_key = self._get_user_api_key()
        layer_name = self._get_resource_id()
        
        payload = {
           "layer_name": layer_name
        }
        
        url = self._get_action_uri() + '/datastore_remove_exposed_layer'
        headers = { 'Authorization': api_key,
                   'X-CKAN-API-Key': api_key,
                   'Content-Type':'application/json'}
        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        
        content = json.loads(response.content)
        result = content["result"]
        return bool(result["success"])
        
    def _REST_datastore_remove_all_exposed_layers(self):
        
        api_key = self._get_user_api_key()
        layer_name = self._get_resource_id()
        
        payload = {}
        
        url = self._get_action_uri() + '/datastore_remove_all_exposed_layers'
        headers = { 'Authorization': api_key,
                   'X-CKAN-API-Key': api_key,
                   'Content-Type':'application/json'}
        
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        
        content = json.loads(response.content)
        
        #print"Content: ",content
        
        result = content["result"]
        return bool(result["success"])
        #return True

# ================================ Utility functions ===============================
    
    # TODO: get this information from the real user, instead of hardcode it    
    def _get_local_engine(self):
        if (self.engine is None):
            data_dict = {}
            data_dict['connection_url'] = pylons.config.get('sqlalchemy.url', 'postgresql://testuser:pass@localhost/testdb')  
            self.engine = db._get_engine(None, data_dict)
            return self.engine
                
    def _execute_sql(self, cls, rscript):
        self._get_local_engine()
        connection = self.engine.connect();
        try:
            print '>>>>>>>>>>>>> Executing command: ', rscript
            trans = connection.begin()
            results = connection.execute(rscript)
            trans.commit() 
        except Exception, e:
            print "exception", e
            assert False
        finally:
            connection.close()
            return results
    
    def _get_user_api_key(self):
        
        script = "select apikey from public.user where name = 'admin';"
        myres = self._execute_sql(self, script)
        for row in myres:
            apikey = row['apikey']
        
        return  apikey
    
    def _get_ckan_base_api_url(self):
        # TODO: read this from the configuration file
        port = self._get_ckan_port()
        hostname = self._get_ckan_hostname()
        
        return "http://" + hostname + ":" + port + "/api"
    
    def _get_action_uri(self):
        base_url = self._get_ckan_base_api_url()
        return base_url + "/action"
    
    def _get_ckan_port(self):
        return str(5000)
    
    def _get_ckan_hostname(self):
        return '127.0.0.1'
    
    def _get_resource_id(self):
        return self.id
   
    def _get_package_name(self):
        return self.package_name
    
    # this function restores the test database to its original state
    # by dropping all tables except geometry_columns and spatial_ref_sys
    def _clean_all_tables_and_packages_in_database(self):
        
    
        base_location = self._get_ckan_base_api_url()
        api_key = self._get_user_api_key()
        testclient = CkanClient(base_location, api_key)
        
        # TODO: clean all packages
         
         # also remove table from database using id
        data_dict = {}
        data_dict['connection_url'] = pylons.config.get('ckan.datastore.write_url', 'postgresql://testuser:pass@localhost/test_datastore')  
        engine = db._get_engine(None, data_dict)
        connection = engine.connect()
        resources_sql = "SELECT * FROM pg_tables;"
        # resources_sql = 'DROP TABLE "b11351a2-5bbc-4f8f-8078-86a4eef1c7b0";'
        try:
            print '>>>>>>>>>>>>> Executing command: ', resources_sql
            trans = connection.begin()
            results_cursor = connection.execute(resources_sql)
            trans.commit() 
            
            allTables = results_cursor.fetchall()
            filteredTables = []
            for table in allTables:
                tableName = table[1]
                if not "pg_" in tableName and not "sql_" in tableName and not tableName == "geometry_columns" and not tableName == "spatial_ref_sys":
                    filteredTables.append(tableName)
            
            trans = connection.begin()        
            for name in filteredTables:
                print "dropping table: ", name
                resource_sql = 'DROP TABLE IF EXISTS "' + name + '";'
                results = connection.execute(resource_sql)
            trans.commit() 
            
        except Exception, e:
            print "exception", e
            assert False
        finally:
            connection.close()
    
    # this function restores the test database to its original state
    # this currently marks the record as deleted but it does not remove it from the databae.
    # a purse must be called in order to clean the database.
    def _clean_test_database(self, package_name, id):
        
        base_location = self._get_ckan_base_api_url()
        api_key = self._get_user_api_key()
        testclient = CkanClient(base_location, api_key)
        # package_name ='spatialize_test_resource_3'
        testclient.package_entity_delete(package_name)
        
         
        # also remove table from database using id
        data_dict = {}
        data_dict['connection_url'] = pylons.config.get('ckan.datastore.write_url', 'postgresql://testuser:pass@localhost/test_datastore')  
        engine = db._get_engine(None, data_dict)
        connection = engine.connect()
        resources_sql = 'DROP TABLE IF EXISTS "' + id + '";'
        # resources_sql = 'DROP TABLE "b11351a2-5bbc-4f8f-8078-86a4eef1c7b0";'
        try:
            print '>>>>>>>>>>>>> Executing command: ', resources_sql
            trans = connection.begin()
            results = connection.execute(resources_sql)
            trans.commit() 
        except Exception, e:
            print "exception", e
            assert False
        finally:
            connection.close()
            
    # this function imports a resource to ckan. the resource will originate a
    # table in the postgres database
    # in order for this to work, don't forget to run paster celeryd before using this function
    def _setup_test_database(self, package_name):
        
        print ">>>>>>>>>>>>>>>>>> creating package: ", package_name
        try:
            base_location = self._get_ckan_base_api_url()
            api_key = self._get_user_api_key()
            testclient = CkanClient(base_location, api_key)
            file_url, status = testclient.upload_file("./testData/small_with_lat_long.csv")
        
            print "created file_url:", file_url
            print "status: ", status
            assert True
            
        except Exception, e:
            print "Exception: ", e
            assert False   
    
        # construct package  and resource json object. set this file path in the resources.
    
        '''    
        package_dict = {u'name': package_name, u'title': u'Spatialize test resource 7', u'notes': u'dummy notes', 
        'owner_org': 'public', u'private': u'False', u'state': u'active', 'extras': {u'status': u'Completed', 
        u'spatial': u'{"type":"Polygon","coordinates":[[[-112.8515625,33.61461929233378],[-112.8515625,35.28150065789119],[-108.28125,35.28150065789119],[-108.28125,33.61461929233378],[-112.8515625,33.61461929233378]]]}'}, 
        'resources': [{'description': u'Resource Document Description','format': u'csv', 'url': file_url, 'name': u'Resouce in alaska3'}]}
        '''
        package_dict = {u'name': package_name, u'title': u'Spatialize test resource 7', u'notes': u'dummy notes',
        'owner_org': 'public', u'private': u'False', u'state': u'active',
        'resources': [{'description': u'Resource Document Description', 'format': u'csv', 'url': file_url, 'name': u'Resource somewhere'}]}
        
        #print "package_dict: at test: ", package_dict
         
        try:
            ret_pack = testclient.package_register_post(package_dict)
            resources = ret_pack['resources']
            database_id = resources[0]['id'] 
        
            print ">>>>>>>>>>>>>>>>>>>>>>>> database_id:", database_id
        except Exception, e:
            print "Exception: ", e
            assert False
            return ""
        
        return database_id
    
# ================================ Main method ===============================
         
'''
This gets executed if one runs this .py file by itself.
This file should be called with the nosetests command, so this code
segment will not be executed by the tests.    
'''

if __name__ == '__main__':
    
    
   
    
    testObj = TestGeoserverIntegration()
    
    package_name = testObj._get_package_name()      
    testObj.setUp()
    
    testObj.test_workspace_and_store_management_functions()
    
    
    testObj.test_datastore_spatialize_scenario()
    
    #testObj._clean_all_tables_in_database()
    
    # testObj.test_datastore_expose_as_layer()
    #testObj.test_datastore_remove_exposed_layer()
    testObj.test_datastore_remove_all_exposed_layers()
    
    # testObj.test_datastore_expose_as_layer()
    # testObj.test_datastore_is_exposed_as_layer()
    
    
    testObj.teardown()
    
    # test_datastore_expose_as_layer()
    # test_datastore_expose_as_layer()
    # test_datastore_list_exposed_layers()
    # test_datastore_remove_exposed_layer()
  
