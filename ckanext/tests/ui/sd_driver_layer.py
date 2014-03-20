""" NGDS_HEADER_BEGIN

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey

Please refer the the README.txt file in the base directory of the NGDS project:
https://github.com/ngds/ckanext-ngds/blob/master/README.txt

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero
General Public License as published by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.  https://github.com/ngds/ckanext-ngds
ngds/blob/master/LICENSE.md or
http://www.gnu.org/licenses/agpl.html

NGDS_HEADER_END """

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class sddriverlayer(unittest.TestCase):
    '''
    classdocs
    Common base class for running Selenium tests with a library of methods to use 
    See also sb_driver_layer
    '''
    
    def SD_setup_webdriver(self):
        ''' Initialize the Selenium web driver as the firefox driver '''
        self.driver = webdriver.Firefox()
        ''' Set how long to wait when trying to locate an element '''
        self.driver.implicitly_wait(30)
        ''' Set the url locations for the central and node under test '''
        self.base_url = "http://node.usgin.org"
        self.central_url = "http://central.usgin.org"
        ''' All errors will be put into this array '''
        self.verificationErrors = []
        ''' Maximize the window to be sure all is displayed '''
        self.SD_maximize_window()
        self.accept_next_alert = True
        self.driver.get(self.base_url)

    def SD_stop_webdriver(self):
        ''' Stop the selenium web driver '''
        self.driver.quit()
        
    def SD_goto_central(self):
        ''' Navigate the browser to the central url '''
        self.driver.get(self.central_url)
        
    def SD_maximize_window(self) :
        ''' Maximize the browser window '''
        self.driver.maximize_window()
        
    def SD_select_link_text(self, linkName):
        ''' Select the link text with this name '''
        self.driver.find_element_by_link_text(linkName).click()
        
    def SD_select_main_menu(self):
        ''' Select the main menu '''
        self.driver.find_element_by_css_selector("span.main-menu-text").click()
               
        
    def SD_select_contribute_page(self):
        ''' Select the contribute page '''
        self.driver.get(self.base_url + "/ngds/contribute")
        
    def SD_select_single_file_upload(self):
        self.driver.find_element_by_css_selector("p.title").click()
        
    def SD_send_keys(self,  elemname, mytitle):
        self.driver.find_element_by_name(elemname).click()
        self.driver.find_element_by_name(elemname).clear()
        self.driver.find_element_by_name(elemname).send_keys(mytitle)
        
    def SD_send_keys_by_id(self,  elemname, mytitle):
        self.driver.find_element_by_id(elemname).click()
        self.driver.find_element_by_id(elemname).clear()
        self.driver.find_element_by_id(elemname).send_keys(mytitle)
    
    def SD_click_preview_button(self):
        self.driver.find_element_by_xpath("(//a[contains(text(),'Preview')])[2]").click()
        
        
    def SD_select_library_page(self):
        ''' Select the NGDS library page - currently fragile as written '''
        self.driver.find_element_by_xpath("//div[@id='main-nav']/nav/a[2]/span/span[2]").click()
    
    def SD_click_login_button(self):
        self.driver.find_element_by_css_selector("button.btn.btn-primary").click()
        
    def SD_click_library_search_button(self):
        self.driver.find_element_by_xpath("//button[@value='Search']").click()
        
    def SD_click_map_search(self):
        self.driver.find_element_by_id("map-search").click()
        
    def SD_select_contribute_page_single_file_upload(self):
        ''' Select the contribute page and then single file upload '''
        self.driver.get(self.base_url + "/ngds/contribute")
        self.driver.find_element_by_css_selector("p.title").click()
        
    def SD_file_upload_enter_title(self, mytitle):
        ''' Enter the title for file upload'''
        self.driver.find_element_by_name("title").clear()
        self.driver.find_element_by_name("title").send_keys(mytitle)
        
           
    def SD_select_tag_group(self, whichGroup):
        ''' Select a tag group on the library page - currently fragile as written '''
        self.driver.find_element_by_xpath("//h3[@id='ui-accordion-search-accoridion-header-" + str(whichGroup) + "']/span").click();
   
    def SD_select_tag_subgroup(self, whichGroup, whichSubGroup):
        ''' Select a checkbox below sub group (below the main tags) on the library page '''
        self.driver.find_element_by_xpath("//div[@id='ui-accordion-search-accoridion-panel-1']/ul/li[3]/div/input").click();
   
    def SD_enter_search_field(self, searchString):
        ''' On the library page, enter a search field and start the search '''
        self.SD_select_library_page()
        self.driver.find_element_by_name("q").clear()
        self.driver.find_element_by_name("q").send_keys(searchString)
        self.driver.find_element_by_xpath("//button[@value='Search']").click()
        
    def SD_enter_map_search_field(self, searchString):
        '''  Enter search field text on the map page and start the search'''
        self.driver.find_element_by_css_selector("span.main-menu-text").click()
        self.driver.find_element_by_id("map-query").clear()
        self.driver.find_element_by_id("map-query").send_keys(searchString)
        self.driver.find_element_by_id("map-search").click()
    
    def SD_click_datalink(self, datalink):
        ''' click on a data link text '''
        self.driver.find_element_by_link_text(datalink).click()
        
    def SD_select_new_window(self):
        ''' When a new window was opened by NGDS such as to view a dataset, switch to the window '''
        self.driver.switch_to_window(self.driver.window_handles[-1])
        
    def SD_select_first_preview(self):
        ''' Select the first Preview button it finds '''
        self.driver.find_element_by_id("dataset-resources")
        self.driver.find_element_by_link_text("Preview").click()
      
          
    def SD_click_wms(self):
        ''' Click the first WMS button it finds '''
        self.driver.find_element_by_xpath("//button[@class='wms ngds-slug']").click()   
        
        
    def SD_click_element_by_id(self, elemId):
        self.driver.find_element_by_id(elemId).click()
        
    def SD_verify_version_info_exists(self):
        ''' Verify that text exists that says what the current version is '''
        versionElement = self.driver.find_element_by_css_selector("#versionInfo > p")
        assert "Tag" in versionElement.text 
            
    def SD_verify_text(self, sString):
        ''' Verify that text exists in the body of the page '''
        verify = r"^[\s\S]*" + sString + "[\s\S]*$"
        try: self.assertRegexpMatches(self.driver.find_element_by_css_selector("BODY").text, verify)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
    def SD_verify_text_not_present(self, sString):
        ''' Verify that the text doesn't appear in the body of the page '''
        verify = r"^[\s\S]*" + sString + "[\s\S]*$"
        try: 
            self.assertRegexpMatches(self.driver.find_element_by_css_selector("BODY").text, verify)
            self.verificationErrors.append("Should not have found text and did")
        except AssertionError as e: print 'Did not find text which is correct'
   

   
  
    
    def SD_verify_iframe_exists_and_does_not_contain_server_error(self):
        ''' Verify that an inner iframe exists and that it does not have text 'server error' in it '''
        iframexists = "false"
        for frame in self.driver.find_elements_by_tag_name('iframe'):
            iframexists = "true"
            try:
                if not frame.is_displayed():
                    continue
                self.driver.switch_to_frame(frame)
                self.SB_verify_text_not_present(self.driver, "server error")
            except:
                pass
        self.driver.switch_to_default_content()
        if iframexists == "false" :
            self.verificationErrors.append("Should have found iframe and did not")
               
               
    def SD_zoom_in(self):
        self.driver.find_element_by_css_selector("a.leaflet-control-zoom-in").click()
             
    def SD_click_on_license_selection(self):   
        self.driver.find_element_by_css_selector("div.controls > div.select2-container > a.select2-choice > div > b").click()
        
    def SD_assert_text_in_license_selection(self):
        try: self.assertEqual("License Not Specified", self.driver.find_element_by_css_selector("div.select2-container.select2-container-active > a.select2-choice > span").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
       
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
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
    
