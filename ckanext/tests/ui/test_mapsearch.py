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


class TestMapSearch(sbpageobjects):
    
    def setUp(self):
        self.SB_setup_webdriver()
        
    
    def test_basic_map_search(self):
        '''Basic test of the map search for data sets'''
        
        self.SB_enter_map_search_field("ohio heat flow")
        self.SB_click_wms()
        
        self.SB_click_datalink("Ohio heat flow demo data")
        
        #select the new window 
        self.SB_select_new_window()
        
        #click the preview button for the first data set TODO need to improve this
        self.SB_select_first_preview();
       
               
        self.SB_verify_iframe_exists_and_does_not_contain_server_error()
                
        self.SB_reset_to_start_page()
        

        
    def tearDown(self):
        self.SB_stop_webdriver()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
