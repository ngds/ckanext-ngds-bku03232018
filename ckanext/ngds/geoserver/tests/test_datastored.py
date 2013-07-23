from ckanext.ngds.tests.ngds_test_case import NgdsTestCase
from ckanext.ngds.geoserver.model.Datastored import Datastored
from ckan.plugins import toolkit
from pylons import config
from sqlalchemy import MetaData, create_engine, Table, Column, Integer

class DatastoredTestCase(NgdsTestCase):
    """
    These tests assume that Geoserver is running either at the default location (localhost:8080/geoserver) or else
    at a location specified in your pylons .ini file

    Also. Datastorer and Harvester don't mix. You will need to have datastorer enabled, which will mean disabling
    ckanext-harvest for these tests

    This will screw around with the datastore table, so you should use a different one in your test.ini file
    """
    datastore_url = config.get("ckan.datastore.write_url")

    def setUp(self):
        self.engine = create_engine(self.datastore_url)
        self.metadata = MetaData()
        self.test_table = Table(
            "test_already",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("lat", Integer),
            Column("lng", Integer)
        )

    def tearDown(self):
        self.metadata.drop_all(self.engine)

    def test_publish_bad_resource_id(self):
        """When asked to publish a resource that is not in the datastore database, should return false"""
        ds = Datastored("fake-as-hell", "nothing", "nothing-else")
        self.assertRaises(toolkit.ObjectNotFound, ds.publish)

    def test_publish_already_published(self):
        """If a resource has already been spatialized, should not fail"""
        # Create a table
        self.test_table.create(self.engine, checkfirst=True)

        # Give it a geometry column
        sql = "select AddGeometryColumn('public', 'test_already', 'geometry', 4326, 'GEOMETRY', 2)"
        conn = self.engine.connect()
        try:
            t = conn.begin()
            conn.execute(sql)
            t.commit()
        except Exception as ex:
            t.rollback()
            conn.close()

        # Now try and "spatialize" it
        ds = Datastored("test_already", "lat", "lng")
        self.assertTrue(ds.publish())

    def test_publish_add_column(self):
        """Publish should add a geometry column to tables that don't have one"""
        # Create a table
        self.test_table.create(self.engine, checkfirst=True)

        # Spatialize it
        ds = Datastored("test_already", "lat", "lng")
        ds.publish()

        # Check that the geometry column exists
        sql = "select count(column_name) from information_schema.columns where table_name='test_already' and column_name='geometry'"
        conn = self.engine.connect()
        res = conn.execute(sql)
        self.assertEqual(res.rowcount, 1)
        for row in res:
            self.assertEqual(row["count"], 1)
        conn.close()