from ckanext.ngds.tests.ngds_test_case import NgdsTestCase
from ckanext.ngds.geoserver.model.Geoserver import Geoserver

class TestGeoserverConnector(NgdsTestCase):
    def test_spatial_tables_exist(self):
        from sqlalchemy import create_engine
        from pylons import config

        engine = create_engine(config.get("sqlalchemy.url"))
        self.assertTrue(engine.dialect.has_table(engine.connect(), "geometry_columns"))

    def test_geoserver_connection(self):
        """Geoserver class method should return a Geoserver instance"""
        gs = Geoserver.from_ckan_config()
        self.assertIsInstance(gs, Geoserver)

    def test_get_default_workspace(self):
        """Geoserver must be able to create or return the default workspace"""
        gs = Geoserver.from_ckan_config()
        ws = gs.default_workspace()
        self.assertEqual(ws.name, "ngds") # should read from config

    def test_package_generator(self):
        p = self.add_package("test-package")
        self.assertIsNotNone(p)