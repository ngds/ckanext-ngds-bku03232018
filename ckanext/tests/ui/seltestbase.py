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
        self.base_url = "http://node.usgin.org"
        self.central_url = "http://central.usgin.org"
        self.verificationErrors = []
        self.SB_maximize_window()
        self.accept_next_alert = True
        self.driver.get(self.base_url)

    
    def SB_maximize_window(self) :
        ''' Maximize the browser window '''
        self.driver.maximize_window()
        
    def SB_reset_to_start_page(self, driver):
        ''' Go to the start page '''
        driver.find_element_by_link_text("Home").click()
        driver.find_element_by_css_selector("span.main-menu-text").click()
    
    def SB_select_about_page(self, driver):
        ''' Select the About page '''
        driver.find_element_by_link_text("About").click()
        
    def SB_select_library_page(self, driver):
        ''' Select the NGDS library page - currently fragile as written '''
        driver.find_element_by_xpath("//div[@id='main-nav']/nav/a[2]/span/span[2]").click()
        
    def SB_select_contribute_page_single_file_upload(self, driver):
        ''' Select the contribute page and then single file upload '''
        driver.get(self.base_url + "/ngds/contribute")
        driver.find_element_by_css_selector("p.title").click()
        
    def SB_file_upload_enter_title(self, driver, mytitle):
        ''' Enter the title for file upload'''
        driver.find_element_by_name("title").clear()
        driver.find_element_by_name("title").send_keys(mytitle)
        
    def SB_file_upload_cancel(self, driver):
        ''' Cancel an in progress file upload'''
        driver.find_element_by_link_text("Cancel").click()
        
    def SB_select_tag_group(self, driver, whichGroup):
        ''' Select a tag group on the library page - currently fragile as written '''
        driver.find_element_by_xpath("//h3[@id='ui-accordion-search-accoridion-header-" + str(whichGroup) + "']/span").click();
   
    def SB_select_tag_subgroup(self, driver, whichGroup, whichSubGroup):
        ''' Select a checkbox below sub group (below the main tags) on the library page '''
        driver.find_element_by_xpath("//div[@id='ui-accordion-search-accoridion-panel-1']/ul/li[3]/div/input").click();
   
    def SB_enter_search_field(self, driver, searchString):
        ''' On the library page, enter a search field and start the search '''
        self.SB_select_library_page(driver)
        driver.find_element_by_name("q").clear()
        driver.find_element_by_name("q").send_keys(searchString)
        driver.find_element_by_xpath("//button[@value='Search']").click()
        
    def SB_enter_map_search_field(self, driver, searchString):
        '''  Enter search field text on the map page and start the search'''
        driver.find_element_by_css_selector("span.main-menu-text").click()
        driver.find_element_by_id("map-query").clear()
        driver.find_element_by_id("map-query").send_keys(searchString)
        driver.find_element_by_id("map-search").click()
    
    def SB_click_datalink(self, driver, datalink):
        ''' click on a data link text '''
        driver.find_element_by_link_text(datalink).click()
        
    def SB_select_new_window(self, driver):
        ''' When a new window was opened by NGDS such as to view a dataset, switch to the window '''
        driver.switch_to_window(driver.window_handles[-1])
        
    def SB_select_first_preview(self, driver):
        ''' Select the first Preview button it finds '''
        driver.find_element_by_id("dataset-resources")
        driver.find_element_by_link_text("Preview").click()
      
          
    def SB_click_wms(self, driver):
        ''' Click the first WMS button it finds '''
        driver.find_element_by_xpath("//button[@class='wms ngds-slug']").click()   
        
        
    def SB_verify_version_info_exists(self, driver):
        ''' Verify that text exists that says what the current version is '''
        versionElement = driver.find_element_by_css_selector("#versionInfo > p")
        assert "Tag" in versionElement.text 
            
    def SB_verify_text(self, driver, sString):
        ''' Verify that text exists in the body of the page '''
        verify = r"^[\s\S]*" + sString + "[\s\S]*$"
        try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, verify)
        except AssertionError as e: self.verificationErrors.append(str(e))
        
    def SB_verify_text_not_present(self, driver, sString):
        ''' Verify that the text doesn't appear in the body of the page '''
        verify = r"^[\s\S]*" + sString + "[\s\S]*$"
        try: 
            self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, verify)
            self.verificationErrors.append("Should not have found text and did")
        except AssertionError as e: print 'Did not find text which is correct'
   

   
  
    def SB_login_as_admin(self, driver):
        ''' Login to the web site '''
        driver.find_element_by_link_text("Login").click()
        
        '''
        all_cookies = driver.get_cookies()
        print "all cookies"
        print all_cookies
        driver.add_cookie({'name' :'ckan' , 'value': '0ca8d46304248fa5024217997efd711b200e3f03221eed4db7a7433e90f099a1ad135539'})
        all_cookies = driver.get_cookies()
        print "all cookies"
        print all_cookies
        '''
        
        driver.find_element_by_name("login").click();
        driver.find_element_by_name("login").clear()
        driver.find_element_by_name("login").send_keys("admin")
        driver.find_element_by_name("password")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("admin")
        #driver.find_element_by_name("remember").click()
        #print "login is"
        #print '#{0}#'.format(driver.find_element_by_name("login").get_attribute('value'))
        #print "password is"
        #print '#{0}#'.format(driver.find_element_by_name("password").get_attribute('value'))
        time.sleep(3)
        #element.fireEvent("onchange");
        #driver.execute_script("document.getElementsByName('login')[0].fireEvent('onchange');")
        #driver.execute_script("document.getElementsByName('password')[0].fireEvent('onchange')")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        #time.sleep(30)
        
    def SB_verify_iframe_exists_and_does_not_contain_server_error(self, driver):
        ''' Verify that an inner iframe exists and that it does not have text 'server error' in it '''
        iframexists = "false"
        for frame in self.driver.find_elements_by_tag_name('iframe'):
            iframexists = "true"
            try:
                if not frame.is_displayed():
                    continue
                driver.switch_to_frame(frame)
                self.SB_verify_text_not_present(driver, "server error")
            except:
                pass
        driver.switch_to_default_content()
        if iframexists == "false" :
            self.verificationErrors.append("Should have found iframe and did not")
                    
            
    def SB_logout(self, driver):
        ''' Logout of the web site '''
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("login-in").click()
        driver.find_element_by_link_text("Logout").click()
  
    '''def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True'''
    
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
