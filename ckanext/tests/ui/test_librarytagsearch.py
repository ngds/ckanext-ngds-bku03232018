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
