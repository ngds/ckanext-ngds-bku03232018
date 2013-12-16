''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''


from sb_page_objects import sbpageobjects
import unittest

class TestTestSetup(sbpageobjects):
    
    def setUp(self):
        self.SB_setup_webdriver()
    
    def test_sel1(self):
        ''' This just starts up the app and enters text in the map query box in order to verify that that setup is working'''
             
        self.SB_enter_map_search_field("wells")
        self.SB_zoom_in()
        self.SB_zoom_in()
           
    
    
    def tearDown(self):
        self.SB_stop_webdriver()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
