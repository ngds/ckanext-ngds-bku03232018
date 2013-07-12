from ckanext.ngds.tests.ngds_test_case import NgdsTestCase
from ckanext.ngds.geoserver.model.ShapeFile import Shapefile
from ckan.controllers import storage
from pylons import config
from datetime import datetime
from osgeo.ogr import DataSource, Layer

import os


test_shapefile_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test-shapefile", "test_shapefile_wgs84.zip"))


class ShapefileTestCase(NgdsTestCase):
    """
    These tests assume that Geoserver is running either at the default location (localhost:8080/geoserver) or else
    at a location specified in your pylons .ini file
    """

    def add_shapefile_resource(self, package_name, filepath=test_shapefile_path):
        # Add a package
        p = self.add_package(package_name)

        # "Upload" shapefile to the package
        ofs = storage.get_ofs()
        label = "%s/test_shapefile_wgs84.zip" % datetime.now().isoformat()
        anything = ofs.put_stream(
            config.get('ckan.storage.bucket', 'default'), # bucket
            label, # label
            open(filepath, "r"), # file stream
            {"key": label} # params
        )

        # Add a resource
        package = self.add_resource(p["id"], {"package_id": p["id"], "url": "http://localhost:5000/storage/f/%s" % label})
        return package.get("resources", [None])[0]

    def setUp(self):
        pass

    def test_shapefile_path_exists(self):
        """Check that creating a shapefile instance finds the path to the compressed file"""
        shapefile_resource = self.add_shapefile_resource("test-path-exists")

        s = Shapefile(shapefile_resource["id"])
        self.assertTrue(os.path.exists(s.file_path))

    def test_shapefile_upload_garbage(self):
        """Garbage in raises an exception (garbage out)"""
        garbage_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test-shapefile", "test_shapefile.dbf"))
        garbage_resource = self.add_shapefile_resource("test-upload-garbage", garbage_path)
        self.assertRaises(Exception, Shapefile, garbage_resource["id"])

    def test_shapefile_dest_source(self):
        """Validate that we can open the datastore database as an OGRDataSource"""
        res = self.add_shapefile_resource("test-dest-source")
        s = Shapefile(res["id"])
        self.assertIsInstance(s.get_destination_source(), DataSource)

    def test_shapefile_dest_layer(self):
        """Check that we can create an OGRLayer in the datastore database"""
        res = self.add_shapefile_resource("test-create-dest-layer")
        s = Shapefile(res["id"])
        ds = s.get_destination_source()
        self.assertIsInstance(s.create_destination_layer(ds, "test-create-dest-layer"), Layer)

    def test_shapefile_dest_layer_fields(self):
        """The destination layer must contain the fields from the source"""
        res = self.add_shapefile_resource("test-dest-fields")
        s = Shapefile(res["id"])
        shapefile = s.get_source_layer().GetLayerDefn()
        source_fields = [shapefile.GetFieldDefn(i).GetName().lower() for i in range(shapefile.GetFieldCount())]

        dest = s.get_destination_layer(s.get_destination_source(), s.get_name()).GetLayerDefn()
        dest_fields = [dest.GetFieldDefn(i).GetName().lower() for i in range(dest.GetFieldCount())]

        self.assertEqual(len(set(source_fields).difference(dest_fields)), 0)

    def test_shapefile_get_dest_layer(self):
        """Check that we can get an OGRLayer in the datastore database"""
        res = self.add_shapefile_resource("test-get-dest-layer")
        s = Shapefile(res["id"])
        ds = s.get_destination_source()
        self.assertIsInstance(s.get_destination_layer(ds, "test-get-dest-layer"), Layer)

    def test_shapefile_publish(self):
        """Publishing a shapefile puts the data into the PostGIS table"""
        res = self.add_shapefile_resource("test-publish")
        s = Shapefile(res["id"])
        self.assertTrue(s.publish())
        self.assertEqual(s.get_source_layer().GetFeatureCount(), s.get_destination_layer().GetFeatureCount())