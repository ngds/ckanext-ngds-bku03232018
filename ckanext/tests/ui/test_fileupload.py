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

class TestFileUpload(sbpageobjects):
    
    def setUp(self):
        self.SB_setup_webdriver()
        self.SB_login_as_admin()
        
        
    
    def test_basic_file_upload_access(self):
        ''' Basic test of file upload access, login and go to page enter title and then cancel '''
        self.SB_select_contribute_page_single_file_upload()
        self.SB_file_upload_enter_title("MyTitle")
        self.SB_file_upload_cancel()

       
    def test_file_upload_licenses_populated(self):
        '''ISSUE-29, assert that license list is filled'''
        self.SB_select_contribute_page_single_file_upload()
        self.SB_click_on_license_selection()
        self.SB_assert_text_in_license_selection()
        self.SB_file_upload_cancel()
               
          

        
    def tearDown(self):
        self.SB_stop_webdriver()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
