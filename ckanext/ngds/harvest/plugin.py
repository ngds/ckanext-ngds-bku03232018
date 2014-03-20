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
from ckan.plugins import IConfigurer, IActions
from ckanext.ngds.harvest.model.harvest_node import define_tables

from ckan import model
from ckanext.ngds.harvest.controllers.ngds_harvest import dispatch, do_harvest


class NgdsHarvestPlugin(SingletonPlugin):
    """Control harvesting operations"""
    
    implements(IConfigurer) # Allows access to configurations (like template locations)
    
    def update_config(self, config):
        """IConfigurable function. config is a dictionary of configuration parameters"""
        # Provides a point to do mappings from classes to database tables whenever CKAN is run
        if not hasattr(model, "HarvestNode"):
            define_tables()
        
    implements(IActions) # Allows us to build a URL and associated binding to a python function
    
    def get_actions(self):
        """IActions function. Should return a dict keys = function name and URL, value is the function to execute"""
        return {
            "ngds_harvest": dispatch,
            "do_harvest": do_harvest
        }
