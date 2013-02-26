from nose.tools import ok_, eq_
import os
import requests, json, ConfigParser

from ckan import plugins
from ckan import model as ckan_model
from ckan.model import meta, Package, Resource, Session

from sqlalchemy import create_engine

class MetadataTestBase(object):
    
    @classmethod
    def setup_class(cls):
        config = ConfigParser.ConfigParser()
        config.read(os.path.join(os.path.dirname( __file__ ), '../../../..', 'test-core.ini'))
        cls.sqlalchemy_url = config.get('app:main', 'sqlalchemy.url')
        cls.host = "127.0.0.1:5000"
        
        script_path = os.path.join(os.path.dirname(os.path.abspath( __file__ )), 'scripts', 'create_tables.sql')
        script = open(script_path, 'r').read()
        cls._execute_sql(script) 
         
    @classmethod
    def _create_record(cls, table):
        data = "(0, 'Genhan Chen', 'genhan.chen@azgs.az.gov', 'Arizona Geological Survey', '520-209-4136', '416 W. Congress St. Ste. 100', 'Tucson', 'AZ', '85701')"
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