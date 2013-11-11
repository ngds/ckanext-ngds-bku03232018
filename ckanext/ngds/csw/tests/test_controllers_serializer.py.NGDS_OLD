from ckanext.ngds.tests.ngds_test_case import NgdsTestCase
from ckanext.ngds.csw.controllers.serializer import PackageSerializer
from lxml import etree

import json

class SerializerTestCase(NgdsTestCase):
    def setUp(self):
        """Do stuff that you want to happen before each test"""
        self.serializer = PackageSerializer()
        pass

    def tearDown(self):
        # Do stuff that you want to happen after each test
        pass

    def test_dispatch_json(self):
        """Test that dispatch function returns valid JSON data"""
        # Make a package
        self.add_package("json-test-package")

        # Spoof the pylons object
        fake_pylons = self.ObjectSpoofer(response=self.ObjectSpoofer(content_type="whatever"))

        # Serialize the package
        oughta_be_json = self.serializer.dispatch(package_id="json-test-package", format="json", pylons=fake_pylons)

        # Check that it is valid JSON
        try:
            json.loads(oughta_be_json)
            self.assertTrue(True)
        except:
            self.assertTrue(
                False,
                "ckanext.ngds.controllers.serializer:PackageSerializer.dispatch did not return a valid json string"
            )

    def test_dispatch_xml(self):
        """Test that dispatch function returns valid XML"""
        self.add_package("xml-test-package")
        fake_response = self.ObjectSpoofer(content_type="whatever")
        fake_pylons = self.ObjectSpoofer(response=fake_response)
        oughta_be_xml = self.serializer.dispatch(package_id="xml-test-package", format="xml", pylons=fake_pylons)
        try:
            etree.fromstring(oughta_be_xml)
            self.assertTrue(True)
        except Exception as ex:
            self.assertTrue(
                False,
                "ckanext.ngds.controllers.serializer:PackageSerializer.dispatch did not return a valid xml string"
            )