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


class TestAboutPage(seltestbase):
    
    def setUp(self):
        self.SB_setup_webdriver()
        
    
    def test_about_page_has_version_identifier(self):
        '''ISSUE-138 About page should identify github version '''
        driver = self.driver
              
        self.SB_select_about_page(driver)
        self.SB_verify_version_info_exists(driver)
         
   
    
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
