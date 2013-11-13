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
import unittest, time, re

class seltestbase(unittest.TestCase):
    '''
    classdocs
    Common base class for running Selenium tests with a library of methods to use 
    '''
    
    def SB_setup_webdriver(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://node.usgin.org/"
        self.central_url = "http://central.usgin.org/"
        self.verificationErrors = []
        self.SB_maximize_window()
        self.accept_next_alert = True
        self.driver.get(self.base_url)

    
    def SB_maximize_window(self) :
        self.driver.maximize_window()
        
    def SB_reset_to_start_page(self, driver):
        driver.find_element_by_link_text("Home").click()
        driver.find_element_by_css_selector("span.main-menu-text").click()
    
        
    def SB_select_library_page(self, driver):
        ''' Select the NGDS library page - currently fragile as written '''
        # TODO add a name or id for location the library link
        #driver.find_element_by_css_selector("span.main-menu-text").click()
        driver.find_element_by_xpath("//div[@id='main-nav']/nav/a[2]/span/span[2]").click()
        
    def SB_select_tag_group(self, driver, whichGroup):
        ''' Select a tag group on the library page - currently fragile as written '''
        driver.find_element_by_xpath("//h3[@id='ui-accordion-search-accoridion-header-" + str(whichGroup) + "']/span");
   
    def SB_select_tag_subgroup(self, driver, whichGroup, whichSubGroup):
        ''' Select a tag sub group (below the main tags) on the library page '''
        self.SB_select_tag_group(driver, whichGroup);
        # //div[@id='ui-accordion-search-accoridion-panel-2']/ul/li[2]/h3
        driver.find_element_by_xpath("//h3[@id='ui-accordion-search-accoridion-header-" + str(whichGroup) + "']/span");
   
    def SB_enter_search_field(self, driver, searchString):
        self.SB_select_library_page(driver)
        driver.find_element_by_name("q").clear()
        driver.find_element_by_name("q").send_keys(searchString)
        driver.find_element_by_xpath("//button[@value='Search']").click()
        
    def SB_verify_text(self, driver, sString):
        verify = r"^[\s\S]*" + sString + "[\s\S]*$"
        try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, verify)
        except AssertionError as e: self.verificationErrors.append(str(e))
        

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
  
  
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
        
 