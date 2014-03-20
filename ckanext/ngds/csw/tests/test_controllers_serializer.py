""" NGDS_HEADER_BEGIN

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey

Please refer the the README.txt file in the base directory of the NGDS project:
https://github.com/ngds/ckanext-ngds/blob/master/README.txt

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero
General Public License as published by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.  https://github.com/ngds/ckanext-ngds
ngds/blob/master/LICENSE.md or
http://www.gnu.org/licenses/agpl.html

NGDS_HEADER_END """

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
