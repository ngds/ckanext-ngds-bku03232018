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

from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer, IActions, IRoutes,IPackageController
from ckanext.ngds.metadata.controllers.additional_metadata import dispatch
from ckanext.ngds.metadata.controllers.transaction_data import dispatch as trans_dispatch

from ckan import model


class MetadataPlugin(SingletonPlugin):
    """The purpose of this plugin is to adjust the metadata content to conform to our standards"""
    
    implements(IConfigurer) # Allows access to configurations (like template locations)
    implements(IRoutes,inherit=True) 

    def update_config(self, config):
        """IConfigurable function. config is a dictionary of configuration parameters"""
        # Provides a point to do mappings from classes to database tables whenever CKAN is run

        if not hasattr(model, "ResponsibleParty"):
            from ckanext.ngds.metadata.model.additional_metadata import define_tables
            define_tables()

            from ckanext.ngds.metadata.model.transaction_tables import define_tables as trans_define_tables
            trans_define_tables()            
        
            # Put IsoPackage into ckan.model for ease of access later
            from ckanext.ngds.metadata.model.iso_package import IsoPackage
            model.IsoPackage = IsoPackage
        
        '''
        # First find the full path to my template directory
        here = os.path.dirname(__file__)
        template_dir = os.path.join(here, "templates") 
        
        # Now add that directory to the extra_template_paths, without removing the existing ones
        config['extra_template_paths'] = ','.join([template_dir, config.get('extra_template_paths', '')])   
        '''

    def before_map(self,map):
        map.connect("responsible_parties","/responsible_parties",controller="ckanext.ngds.metadata.controllers.additional_metadata:Responsible_Parties_UI",action="get_responsible_parties",conditions={"method":["GET"]})   
        map.connect("languages","/languages",controller="ckanext.ngds.metadata.controllers.additional_metadata:Languages_UI",action="get_languages",conditions={"method":["GET"]})   
        return map
    
    implements(IActions) # Allows us to build a URL and associated binding to a python function
    
    def get_actions(self):
        """IActions function. Should return a dict keys = function name and URL, value is the function to execute"""
        return {
            "additional_metadata": dispatch,
            "transaction_data": trans_dispatch
        }
