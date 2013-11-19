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


class TestBrowsingResources(seltestbase):
    
    def setUp(self):
        self.SB_setup_webdriver()
        
    
    def test_failed_resource_viewing(self):
        '''ISSUE-86 Browsing resource causes internal server error on central node'''
        driver = self.driver
        # go to central site where the issue was
        self.driver.get(self.central_url)
              
        self.SB_enter_search_field(driver, "California Active Faults")
        #driver.find_element_by_link_text("California Active Faults").click()
        self.SB_click_datalink(driver, "California Active Faults")
        driver.find_element_by_xpath("(//a[contains(text(),'Preview')])[2]").click()
        time.sleep(25)
        self.SB_verify_iframe_exists_and_does_not_contain_server_error(driver)
        
        
      
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
