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


class TestLibrarySearch(seltestbase):
    
    def setUp(self):
        self.SB_setup_webdriver()
        
    
    def test_basic_library_search(self):
        '''Basic test of the library search for data sets'''
        driver = self.driver
              
        self.SB_enter_search_field(driver, "Virginia")
        self.SB_verify_text(driver, "dataset found")
        self.SB_enter_search_field(driver,"AkJDKDJSDpioSDLKJFSDLKJF")
        self.SB_verify_text(driver, "no datasets found for")
        #self.SB_reset_to_start_page(driver)
        
    def test_nevada_search_error(self):
        '''Test for issue 28, Nevada search causing server error'''
        driver = self.driver
        # go to central site where the issue was
        self.driver.get(self.central_url)
        self.SB_enter_search_field(driver, "Nevada")
        self.SB_verify_text(driver, "datasets found")
    
    '''
    def test_tagged_search(self):
        #Basic test of library search using tags 
        driver = self.driver
        
        self.SB_select_library_page(driver);
        self.SB_select_tag_group(driver, 2);
        self.SB_select_tag_group(driver, 3);
        self.SB_select_tag_subgroup(driver, 3, 1);
        self.SB_verify_text(driver, "dataset found")
        
    '''  
        
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
