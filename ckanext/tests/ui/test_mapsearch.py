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
        self.SB_enter_map_search_field(driver, "ohio heat flow")
        self.SB_click_wms(driver)
        
        self.SB_click_datalink(driver, "Ohio heat flow demo data")
        
        #select the new window 
        self.SB_select_new_window(driver)
        
        #click the preview button for the first data set TODO need to improve this
        self.SB_select_first_preview(driver);
       
               
        self.SB_verify_iframe_exists_and_does_not_contain_server_error(driver)
                
        self.SB_reset_to_start_page(driver)
        

        
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
