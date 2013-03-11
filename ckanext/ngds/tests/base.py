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
    
    @classmethod
    def setup_class(cls):
        cls.sqlalchemy_url = config.get("sqlalchemy.url")
        #cls.host = "127.0.0.1:5000"      
        
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