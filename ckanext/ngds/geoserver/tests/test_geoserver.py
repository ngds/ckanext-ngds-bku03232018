from ckanext.ngds.tests.ngds_test_case import NgdsTestCase
from ckanext.ngds.geoserver.model.Geoserver import Geoserver

class TestGeoserverConnector(NgdsTestCase):
    """
    These tests assume that Geoserver is running either at the default location (localhost:8080/geoserver) or else
    at a location specified in your pylons .ini file
    """

    def setUp(self):
        self.gs = Geoserver.from_ckan_config()

    def test_get_default_workspace(self):
        """Geoserver must be able to create or return the default workspace"""
        ws = self.gs.default_workspace()
        self.assertEqual(ws.name, "ngds") # should read from config

    def test_get_default_datastore(self):
        """Geoserver must be able to create or return the default datastore"""
        ds = self.gs.default_datastore()
        self.assertIsNotNone(ds)