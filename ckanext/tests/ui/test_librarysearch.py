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
        driver.get(self.base_url + "/")
        
        self.SB_enter_search_field(driver, "Virginia")
        # Warning: verifyTextPresent may require manual changes
        try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*dataset found for[\s\S]*$")
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.SB_enter_search_field(driver, "Arkansas")
        self.SB_enter_search_field(driver,"AkJDKDJSDpioSDLKJFSDLKJF")
        # Warning: verifyTextPresent may require manual changes
        try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*no datasets found for[\s\S]*$")
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.SB_reset_to_start_page(driver)
   
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
