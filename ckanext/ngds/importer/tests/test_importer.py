''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

import os

from nose.tools import *

from ckanext.ngds.importer.importer import BulkUploader
from ckanext.ngds.tests.ngds_test_case import NgdsTestCase


class ImporterTestCase(NgdsTestCase):

    # Use this method to initialize the database
    def setUp(self):
        print ">>>>>>>>> Test Steup >>>>>>>>"
        assert True


    # Use this method to reset the database
    def teardown(self):
        print ">>>>>>>>>> Test Teardown >>>>>>>"
        assert True

    def test_loadclientconfig(self):
        client_config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata", "ckanclient.cfg"))
        bulkuploader = BulkUploader(client_config=client_config_path)
        assert_equals(bulkuploader.url, 'http://localhost:5000/api')
        assert_equals(bulkuploader.api_key, '5364e36d-0bd0-43af-be38-452149466950')


    @raises(Exception)
    def test_loadclientconfig_1(self):
        client_config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata", "ckanclient_without_url.cfg"))
        bulkuploader = BulkUploader(client_config=client_config_path)

    @raises(Exception)
    def test_loadclientconfig_2(self):
        client_config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata", "ckanclient_without_api.cfg"))
        bulkuploader = BulkUploader(client_config=client_config_path)

    @raises(Exception)
    def test_loadclientconfig_3(self):
        client_config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata", "ckanclient_without_host.cfg"))
        bulkuploader = BulkUploader(client_config=client_config_path)

    # def test_execute_bulk_upload():
    #     client_config_path= "./testdata/ckanclient_without_host.cfg"
    #     bulkuploader = BulkUploader(client_config=client_config_path)

    '''
        def _clean_test_database(self, package_name, id):

            base_location = self._get_ckan_base_api_url()
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
                trans = connection.begin()
                results = connection.execute(resources_sql)
                trans.commit()
            except Exception, e:
                print "exception",e
                assert False
            finally:
                connection.close()

    '''
