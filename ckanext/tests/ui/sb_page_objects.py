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

from sd_driver_layer import sddriverlayer
import time
 
class sbpageobjects(sddriverlayer):
    '''
    classdocs
    Common base class for running Selenium tests with a library of methods to use 
    See also sb_driver_layer
    '''
        
    def SB_setup_webdriver(self):
        ''' basic web driver initialization call '''
        self.base_url = "http://node.usgin.org"
        self.central_url = "http://central.usgin.org"
        self.SD_setup_webdriver()

        
    def SB_stop_webdriver(self):
        ''' stop the web driver '''
        self.SD_stop_webdriver()
        
        
    def SB_reset_to_start_page(self):
        ''' Go to the start page '''
        self.SD_click_datalink("Home")
        self.SD_select_main_menu()
        
    def SB_goto_central(self):
        ''' Go to the central web site for NGDS '''
        self.SD_goto_central()
        
    def SB_zoom_in(self):
        ''' Zoom in to the map closer '''
        self.SD_zoom_in()
        
    def SB_select_about_page(self):
        ''' Select the About page '''
        self.SD_click_datalink("About")
        
        
    def SB_select_library_page(self):
        ''' Select the NGDS library page  '''
        self.SD_select_library_page()
        
        
    def SB_select_contribute_page_single_file_upload(self):
        ''' Select the contribute page and then single file upload '''
        self.SD_select_contribute_page()
        self.SD_select_single_file_upload()
        
    def SB_click_preview_button(self):
        ''' Assumes the preview button is visible and clicks it '''
        self.SD_click_preview_button()
        
    def SB_file_upload_enter_title(self, mytitle):
        ''' Enter the title for file upload'''
        self.SD_send_keys("title", mytitle)
        
        
    def SB_file_upload_cancel(self):
        ''' Cancel an in progress file upload'''
        self.SD_select_link_text("Cancel")
        
        
    def SB_select_tag_group(self, whichGroup):
        ''' Select a tag group on the library page '''
        self.SD_select_tag_group(whichGroup);
        
   
    def SB_select_tag_subgroup(self,  whichGroup, whichSubGroup):
        ''' Select a checkbox below sub group (below the main tags) on the library page '''
        self.SD_select_tag_subgroup(whichGroup, whichSubGroup)
        
    def SB_enter_search_field(self, searchString):
        ''' On the library page, enter a search field and start the search '''
        self.SB_select_library_page()
        self.SD_send_keys("q", searchString)
        self.SD_click_library_search_button()
        
        
    def SB_enter_map_search_field(self, searchString):
        '''  Enter search field text on the map page and start the search'''
        self.SD_select_main_menu()
        self.SD_send_keys_by_id("map-query", searchString);
        self.SD_click_map_search()
        
    
    def SB_click_datalink(self, datalink):
        ''' click on a data link text '''
        self.SD_click_datalink(datalink)
        
        
    def SB_select_new_window(self):
        ''' When a new window was opened by NGDS such as to view a dataset, switch to the window '''
        self.SD_select_new_window()
        
    def SB_select_first_preview(self):
        ''' Select the first Preview button it finds '''
        self.SD_select_first_preview()
        
      
          
    def SB_click_wms(self):
        ''' Click the first WMS button it finds '''
        self.SD_click_wms()
         
        
        
    def SB_verify_version_info_exists(self):
        ''' Verify that text exists that says what the current version is '''
        self.SD_verify_version_info_exists()
        
            
    def SB_verify_text(self, sString):
        ''' Verify that text exists in the body of the page '''
        self.SD_verify_text(sString)
        
        
    def SB_verify_text_not_present(self, sString):
        ''' Verify that the text doesn't appear in the body of the page '''
        self.SD_verify_text_not_present(sString)
       
   
  
    def SB_login_as_admin(self):
        ''' Login to the web site '''
        self.SD_click_datalink("Login")
        
        
        '''
        all_cookies = driver.get_cookies()
        print "all cookies"
        print all_cookies
        driver.add_cookie({'name' :'ckan' , 'value': '0ca8d46304248fa5024217997efd711b200e3f03221eed4db7a7433e90f099a1ad135539'})
        all_cookies = driver.get_cookies()
        print "all cookies"
        print all_cookies
        '''
        self.SD_send_keys( "login", "admin")
        self.SD_send_keys("password", "admin")
        
        #driver.find_element_by_name("remember").click()
        #print "login is"
        #print '#{0}#'.format(driver.find_element_by_name("login").get_attribute('value'))
        #print "password is"
        #print '#{0}#'.format(driver.find_element_by_name("password").get_attribute('value'))
        time.sleep(3)
        #element.fireEvent("onchange");
        #driver.execute_script("document.getElementsByName('login')[0].fireEvent('onchange');")
        #driver.execute_script("document.getElementsByName('password')[0].fireEvent('onchange')")
        self.SD_click_login_button()
        
        #time.sleep(30)
        
    def SB_verify_iframe_exists_and_does_not_contain_server_error(self):
        ''' Verify that an inner iframe exists and that it does not have text 'server error' in it '''
        self.SD_verify_iframe_exists_and_does_not_contain_server_error()
        
                    
            
    def SB_logout(self):
        ''' Logout of the web site '''
        self.SD_click_datalink("Login")
        self.SD_click_element_with_id("login-in")
        self.SD_click_datalink("Logout")
        
    def SB_click_on_license_selection(self):
        self.SD_click_on_license_selection()
    
    def SB_assert_text_in_license_selection(self):
        self.SD_assert_text_in_license_selection()
  
