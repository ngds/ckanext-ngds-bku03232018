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


class TestLibrarySearch(sbpageobjects):
    
    def setUp(self):
        self.SB_setup_webdriver()
        
    
    def test_basic_library_search(self):
        '''Basic test of the library search for data sets'''
        
              
        self.SB_enter_search_field("Virginia")
        self.SB_verify_text_not_present("no datasets found")
        self.SB_enter_search_field("AkJDKDJSDpioSDLKJFSDLKJF")
        self.SB_verify_text( "no datasets found for")
        
        
    def test_nevada_search_error(self):
        '''ISSUE-28 Nevada search causing server error on central node'''
       
        # go to central site where the issue was
        self.SB_goto_central()
        self.SB_enter_search_field("Nevada")
        self.SB_verify_text("datasets found")
    
    
    def tearDown(self):
        self.SB_stop_webdriver()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
