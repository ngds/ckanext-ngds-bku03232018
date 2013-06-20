from ckanext.ngds.tests.ngds_test_case import NgdsTestCase

class TestGeoserverConnector(NgdsTestCase):
    def setUp(self):
        self.ngds_table_set_up()

    def test_spatial_tables_exist(self):
        from sqlalchemy import create_engine
        from pylons import config

        engine = create_engine(config.get("sqlalchemy.url"))
        self.assertTrue(engine.dialect.has_table(engine.connect(), "geometry_columns"))

