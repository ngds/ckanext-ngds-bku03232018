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
import unittest, time

class TestBrowsingResources(sbpageobjects):
    
    def setUp(self):
        self.SB_setup_webdriver()
        
    
    def test_failed_resource_viewing(self):
        '''ISSUE-86 Browsing resource causes internal server error on central node'''
        
        # go to central site where the issue was
        self.SB_goto_central()
        
        self.SB_enter_search_field("California Active Faults")
        
        self.SB_click_datalink("California Active Faults")
        self.SB_click_preview_button()
        time.sleep(25)
        self.SB_verify_iframe_exists_and_does_not_contain_server_error()
      
      
    
    def tearDown(self):
        self.SB_stop_webdriver()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
