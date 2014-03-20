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

'''
Created on Jun 17, 2013

@author: 
'''
import unittest
import time
import pylons
import os
import ckan.model as model
from ckan import plugins
import requests, json, ConfigParser
from pylons import config
from ckanext.ngds.csw.controllers.serializer import PackageSerializer

from ckanclient import CkanClient
import ckanext.datastore.db as db

from sqlalchemy import create_engine

from paste.deploy import appconfig
from pylons import config


#conf = appconfig('config:development.ini', relative_to='../../../../../ckan/.')

# Note that paster must have started ckan for this test to be able to execute
# e.g. start paster separately
class TestPackageSerialization(unittest.TestCase):
	millis = int(round(time.time() * 1000))
	package_name = 'serializer_test_resource_' + str(millis)
	id = ""  # id of the resource used during testing
	database_id = ""
	engine = None
	
	def setUp(self):
		print ">>>>>>>>> Test Setup >>>>>>>>"
		self.id = self._setup_test_database(self.package_name)
        time.sleep(2)  # wait for the data to be stored in the database through celeryd
        #plugins.load('csw')
        
        assert True


	def tearDown(self):
		print ">>>>>>>>>> Test Teardown >>>>>>>"
		# time.sleep(1) # wait for the database to be updated
		self._clean_test_database(self.package_name, self.id)
		assert True


	def testSerialize(self):
		# so this doesn't work because ckan isn't initiazed as what is running in this
		# test, so when it tries to look up the package it fails
		# so change this to a web service call as in the test_geoserver tests
		# and for this case, give up trying to invoke the controller directly
		# because if you attempt to run nosetests with --ckan, it trashes the databases by
		# removing the postGIS tab;es, etc.
		'''pkg = model.Package.get(self.database_id)
		package_serializer=PackageSerializer()
		returnVal = package_serializer.dispatch(format='xml', package_id=self.database_id)
		#package_id=self.database_id)
		print ">>>> ", returnVal
		'''
		assert True

	# this function imports a resource to ckan. the resource will originate a
	# table in the postgres database
	def _setup_test_database(self, package_name):
		
		print ">>>>>>>>>>>>>>>>>> creating package: ", package_name
		base_location = self._get_ckan_base_api_url()
		api_key = self._get_user_api_key()
		testclient = CkanClient(base_location, api_key)
		print "base.. ", testclient.base_location
		file_url, status = testclient.upload_file("./testData/small_with_lat_long.csv")
		
		print "created file_url:", file_url
		print "status: ", status
		assert True
		  
	
		package_dict = {u'name': package_name, u'title': u'Serialize test 1', u'notes': u'dummy notes',
		'owner_org': 'public', u'private': u'False', u'state': u'active',
		'resources': [{'description': u'Resource Document Description', 'format': u'csv', 'url': file_url, 'name': u'Resource somewhere'}]}
		
		#print "package_dict: at test: ", package_dict
		 
		try:
			ret_pack = testclient.package_register_post(package_dict)
			resources = ret_pack['resources']
			self.database_id = resources[0]['id'] 
		
			print ">>>>>>>>>>>>>>>>>>>>>>>> database_id:", self.database_id
		except Exception, e:
			print "Exception: ", e
			assert False
			return ""
		
		return self.database_id
	
	def _get_ckan_base_api_url(self):
		port = self._get_ckan_port()
		hostname = self._get_ckan_hostname()
		
		return "http://" + hostname + ":" + port + "/api"
	
	def _get_ckan_port(self):
		return str(5000)
	
	def _get_ckan_hostname(self):
		return 'localhost'
	
	def _get_resource_id(self):
		return self.id
   
	def _get_package_name(self):
		return self.package_name

	def _clean_test_database(self, package_name, id):
		
		base_location = self._get_ckan_base_api_url()
		api_key = self._get_user_api_key()
		testclient = CkanClient(base_location, api_key)
		# package_name ='spatialize_test_resource_3'
		testclient.package_entity_delete(package_name)
        	# also remove table from database using id
        	data_dict = {}
       		data_dict['connection_url'] = pylons.config.get('ckan.datastore.write_url', 'postgresql://testuser:pass@localhost/testdb')  
        	self.engine = db._get_engine(None, data_dict)
        	connection = self.engine.connect()
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

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
