import datetime
import sqlalchemy.orm as orm
from sqlalchemy import Table

from ckanext.ngds.common import plugins
#from ckanext.ngds.common import tests
import ckan.tests as tests
from ckanext.ngds.common import model
from ckanext.ngds.common import config
from ckanext.ngds.common import app_globals
from ckanext.ngds.common import base

import ckanext.ngds.sysadmin.model.db as db

_ = base._

class TestSysadmin(tests.WsgiAppCase):
    @classmethod
    def setup_class(cls):
        # Load sysadmin plugin
        plugins.load('ngds_sysadmin')

    @classmethod
    def teardown_class(self):
        # Rebuild DB and unload sysadmin plugin
        model.repo.rebuild_db()
        plugins.unload('ngds_sysadmin')

    def test_build_table_and_orm(self):
        # Check if 'ngds_system_info' table exists, build it if it doesn't
        table = Table('ngds_system_info', model.meta.metadata)
        if not table.exists():
            db.init(model)
        assert(table.exists())

    def test_populate_table_with_defaults_and_dictize(self):
        # Register NGDS configs with pylons global config
        app_globals.mappings['ngds.publish'] = 'ngds.publish'
        app_globals.mappings['ngds.harvest'] = 'ngds.harvest'
        app_globals.mappings['ngds.edit_metadata'] = 'ngds.edit_metadata'

        # Make dictionary of configs with default values to initialize the
        # 'ngds_system_info' table
        data = {
            'ngds.publish': config.get('ngds.publish', 'True'),
            'ngds.harvest': config.get('ngds.harvest', 'True'),
            'ngds.edit_metadata': config.get('ngds.edit_metadata', 'True'),
        }

        # Populate that sucka
        db.init_table_populate(model, data)

        # Hocus pocus magic to make sure that the 'ngds_system_info' table was
        # populated with the correct values
        db_config = {}
        table = db.SysadminConfig.get(active_config=True)
        mapped_table = orm.class_mapper(table.__class__).mapped_table
        for key in mapped_table.c.keys():
            db_config[key] = getattr(table, key)

        assert db_config.get('ngds.publish') == 'True'
        assert db_config.get('ngds.harvest') == 'True'
        assert db_config.get('ngds.edit_metadata') == 'True'

    def test_update_table_with_new_values(self):
        # Make some dummy data and see if we can update the 'ngds_system_info'
        # table with new values
        data_controls = [{'text': 'Enabled', 'value': 'True'},
                         {'text': 'Disabled', 'value': 'False'}]

        items = [{'name': 'ngds.publish', 'control': 'select', 'options': data_controls, 'label': _('Data Publishing'), 'placeholder': ''},
                 {'name': 'ngds.harvest', 'control': 'select', 'options': data_controls, 'label': _('Data Harvesting'), 'placeholder': ''},
                 {'name': 'ngds.edit_metadata', 'control': 'select', 'options': data_controls, 'label': _('Metadata Editing'), 'placeholder': ''}]

        data = {'ngds.publish': u'False', 'ngds.harvest': u'False', 'ngds.edit_metadata': u'False', 'save-data-config': u''}

        update_db = db.SysadminConfig.get(active_config=True)

        for item in items:
            name = item['name']
            if name in data:
                # Update app_globals in memory
                app_globals.set_global(name, data[name])
                # Update database
                setattr(update_db, name, data.get(name))
        app_globals.reset()
        update_db.last_edited = datetime.datetime.utcnow()
        update_db.save()
        session = model.Session
        session.add(update_db)
        session.commit()
        
        # Hocus pocus magic to make sure that the 'ngds_system_info' table was
        # populated with the correct values
        db_config = {}
        table = db.SysadminConfig.get(active_config=True)
        mapped_table = orm.class_mapper(table.__class__).mapped_table
        for key in mapped_table.c.keys():
            db_config[key] = getattr(table, key)

        assert db_config.get('ngds.publish') == 'False'
        assert db_config.get('ngds.harvest') == 'False'
        assert db_config.get('ngds.edit_metadata') == 'False'
