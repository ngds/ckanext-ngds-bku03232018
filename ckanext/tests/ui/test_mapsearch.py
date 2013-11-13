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


class TestMapSearch(seltestbase):
    
    def setUp(self):
        self.SB_setup_webdriver()
        
    
    def test_basic_map_search(self):
        '''Basic test of the map search for data sets'''
        driver = self.driver
        driver.get(self.base_url + "/")
        
        driver.find_element_by_css_selector("span.main-menu-text").click()
        driver.find_element_by_id("map-query").clear()
        driver.find_element_by_id("map-query").send_keys("heat flow")
        driver.find_element_by_id("map-search").click()
        driver.find_element_by_xpath("//button[@class='wms ngds-slug']").click()
        driver.find_element_by_link_text("Ohio heat flow demo data").click()
        #select the new window 
        driver.switch_to_window(driver.window_handles[-1])
        #click the preview button for the first data set TODO need to improve this
        driver.find_element_by_id("dataset-resources")
        driver.find_element_by_link_text("Preview").click()
        # remove this one have some kind of assert that we found the data
        time.sleep(10)
        #driver.find_element_by_xpath("//a[text()='Preview']").click()
        #driver.find_element_by_css_selector("a.leaflet-popup-close-button").click()
        self.SB_reset_to_start_page(driver)
        

        
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
