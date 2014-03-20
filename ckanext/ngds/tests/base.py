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

from nose.tools import ok_, eq_
import os
import requests, json, ConfigParser

from ckan import plugins
from ckan import model
from ckan.logic.action.create import package_create
from ckan.logic.schema import default_create_package_schema
from ckan.model import meta, Package, Resource, Session
from ckan.tests import CreateTestData

from sqlalchemy import create_engine
from pylons import config

from ckanext.ngds.base.commands.ngds_tables import NgdsTables


class MetadataTestBase(object):
    sqlalchemy_url = config.get("sqlalchemy.url")
    
    @classmethod
    def setup_class(cls):     
        
        script_path = os.path.join(os.path.dirname(os.path.abspath( __file__ )), 'scripts', 'create_tables.sql')
        script = open(script_path, 'r').read()
        cls._execute_sql(script)
        
        #CreateTestData.create_test_user()
        
        '''
        schema = default_create_package_schema()
        context = {
                'model': model,
                'session': Session,
                'user': 'tester',
                'schema': schema,
                'api_version': 2
            }
        '''
        package_fixture_data =  {
                'name': 'test-ngds',
                'title': 'test title',
                'resources': [
                        {
                            'name': 'test-resource',
                            'url': 'http://azgs.az.gov',
                            'format': 'plain text',
                            'description': 'This is a test description',
                            'hash': 'abc123',
                            'extras': {'size_extra': '123'}
                        }
                    ]
            }
        
        '''
        package_dict = package_create(context, package_fixture_data)
        cls.package_id = context.get('id') 
        '''
        CreateTestData.create_arbitrary(package_fixture_data)
        
    @classmethod
    def teardown_class(cls):
        script = "DROP TABLE IF EXISTS package_additional_metadata, resource_additional_metadata, responsible_party, languages, harvested_record, harvest_node, spatial_ref_sys, geometry_columns"
        cls._execute_sql(script)

    @classmethod
    def _create_record(cls, table, data):
        #data = "(0, 'Genhan Chen', 'genhan.chen@azgs.az.gov', 'Arizona Geological Survey', '520-209-4136', '416 W. Congress St. Ste. 100', 'Tucson', 'AZ', '85701')"
        script = "INSERT INTO %s VALUES %s" % (table, data)
        cls._execute_sql(script)         

    @classmethod
    def _delete_record(cls, table, record_id):
        script = "DELETE FROM %s WHERE id = %d" % (table, record_id)
        cls._execute_sql(script)

    @classmethod
    def _execute_sql(cls, script):
        engine = create_engine(cls.sqlalchemy_url)
        Session.bind = engine
        
        connection = Session.connection()

        connection.execute(script)
        Session.commit() 
