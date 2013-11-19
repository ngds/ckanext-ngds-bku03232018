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
        
        
    
    def test_basic(self):
        '''Basic test of the map search for data sets'''
        driver = self.driver
        driver.get(self.base_url + "/")
        # login is not working, needs to pass a cookie that its not
        self.SB_login_as_admin(driver)
        #driver.find_element_by_css_selector("p.title").click()
        #driver.find_element_by_xpath("//div[@id='main-nav']/nav/a[4]/span/span").click()
        time.sleep(10)       

        
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
