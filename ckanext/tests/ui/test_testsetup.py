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

class TestTestSetup(seltestbase):
    
    def setUp(self):
         self.SB_setup_webdriver()
    
    def test_sel1(self):
        ''' This just starts up the app and enters text in the map query box in order to verify that that setup is working'''
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_css_selector("span.main-menu-text").click()
        driver.find_element_by_id("map-query").click()
        driver.find_element_by_id("map-query").clear()
        driver.find_element_by_id("map-query").send_keys("wells")
        driver.find_element_by_css_selector("a.leaflet-control-zoom-in").click()
        driver.find_element_by_css_selector("a.leaflet-control-zoom-in").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
