from ckanext.ngds.tests.ngds_test_case import NgdsTestCase
from ckanext.ngds.geoserver.model.ShapeFile import Shapefile
from ckan.controllers import storage
from pylons import config
from datetime import datetime
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
