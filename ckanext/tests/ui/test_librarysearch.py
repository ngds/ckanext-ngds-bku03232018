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
