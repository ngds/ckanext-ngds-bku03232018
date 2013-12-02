''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from seltestbase import seltestbase
import unittest, time, re

class TestFileUpload(seltestbase):
    
    def setUp(self):
        self.SB_setup_webdriver()
        driver = self.driver
        self.SB_login_as_admin(driver)
        
        
    
    def test_basic_file_upload_access(self):
        ''' Basic test of file upload access, login and go to page enter title and then cancel '''
        driver = self.driver
        self.SB_select_contribute_page_single_file_upload(driver)
        self.SB_file_upload_enter_title(driver, "MyTitle")
        self.SB_file_upload_cancel(driver)

       
    def test_file_upload_licenses_populated(self):
        '''ISSUE-29, assert that license list is filled'''
        driver = self.driver
        self.SB_select_contribute_page_single_file_upload(driver)
        driver.find_element_by_css_selector("div.controls > div.select2-container > a.select2-choice > div > b").click()
        try: self.assertEqual("License Not Specified", driver.find_element_by_css_selector("div.select2-container.select2-container-active > a.select2-choice > span").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.SB_file_upload_cancel(driver)
               
          

        
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
