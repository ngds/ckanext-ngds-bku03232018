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


class TestAboutPage(sbpageobjects):
    
    def setUp(self):
        self.SB_setup_webdriver()
        
    
    def test_about_page_has_version_identifier(self):
        '''ISSUE-138 About page should identify github version '''
                      
        self.SB_select_about_page()
        self.SB_verify_version_info_exists()
 
    def tearDown(self):
        self.SB_stop_webdriver()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
