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

class TestLibraryTagSearch(seltestbase):
    
    def setUp(self):
        self.SB_setup_webdriver()
    
    
    def test_tagged_search(self):
        #Basic test of library search using tags 
        driver = self.driver
        
        self.SB_select_library_page(driver);
        #self.SB_select_tag_group(driver, 0);
        self.SB_select_tag_group(driver, 1);
        #self.SB_select_tag_subgroup(driver, 1, 1);
        self.SB_verify_text(driver, " found")
        # this is just to visually verify test verify is working, remove 
        time.sleep(10)
        
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
