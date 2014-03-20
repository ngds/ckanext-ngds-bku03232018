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


from sb_page_objects import sbpageobjects
import unittest

class TestLibraryTagSearch(sbpageobjects):
    
    def setUp(self):
        self.SB_setup_webdriver()
    
    
    def test_tagged_search(self):
        #Basic test of library search using tags 
        
        self.SB_select_library_page();
        #self.SB_select_tag_group(driver, 0);
        # This test needs additional development 
        # as its not ccorrectly finding the tags
        #self.SB_select_tag_group(1);
        #self.SB_select_tag_subgroup(driver, 1, 1);
        #self.SB_verify_text(" found")
        
        
    def tearDown(self):
        self.SB_stop_webdriver()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
