import nose
import paste.fixture

from ckanext.ngds.common import plugins
from ckanext.ngds.common import tests
from ckanext.ngds.common import model
from ckanext.ngds.common import config
from ckanext.ngds.common import middleware

import ckanext.ngds.sysadmin.controllers.admin as db
import ckanext.ngds.sysadmin.model.db as db


class TestSysadmin(tests.WsgiAppCase):
    @classmethod
    def setup_class(cls):
        wsgiapp = middleware.make_app(config['global_conf'], **config)
        cls.app = paste.fixture.TestApp(wsgiapp)

        plugins.load('sysadmin')

        cls.sysadmin_user = model.User.get('testsysadmin')
        engine = db.

    def setup(self):
        model.repo.rebuild_db()

    def test_build_table_and_orm(self):

        pass

    def test_populate_table_with_defaults(self):
        pass

    def test_read_table_and_dictize(self):
        pass

    def test_update_table_with_new_values(self):
        pass

