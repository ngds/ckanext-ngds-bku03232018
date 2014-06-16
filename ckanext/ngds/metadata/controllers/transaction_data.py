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

from ckan.plugins.toolkit import toolkit
from ckanext.ngds.base.controllers.ngds_crud_controller import NgdsCrudController

def dispatch(context, data_dict):
    """
    Send the action request to the correct place, based on the POST body
    
    Body should contain JSON data as follows:
    {
      "model": One of BulkUpload
      "process": One of "create", "read", "update", "delete"
      "data": An object containing the data to act on
    }
    
    Requests are inspected and passed on to model-specific controllers, defined below
    
    """
    
    # Determine the correct controller by inspecting the data_dict
    request_model = data_dict.get("model", None)
    controller = None
    print "request_model: ",request_model
    if request_model == "BulkUpload":
        controller = BulkUploadController(context)
    elif request_model == "BulkUpload_Package":
        controller = BulkUpload_PackageController(context)
    elif request_model == "StandingData":
        controller = StandingDataController(context)
    elif request_model == "UserSearch":
        controller = UserSearchController(context)
    elif request_model == "DocumentIndex":
        controller = DocumentIndexController(context)
    else:
        raise toolkit.ValidationError({}, "Please supply a 'model' attribute in the POST body. Value can be one of: BulkUpload,BulkUpload_Package,StandingData,UserSearch,DocumentIndex")
    
    # execute method inspects POST body and runs the correct functions
    return controller.execute(data_dict)

class BulkUploadController(NgdsCrudController):
    """Controls CRUD API for BulkUpload"""
    def __init__(self, context):
        """Find the right model for this class"""
        self.model = context['model'].BulkUpload

class BulkUpload_PackageController(NgdsCrudController):
    """Controls CRUD API for BulkUpload_PackageController"""
    def __init__(self, context):
        """Find the right model for this class"""
        self.model = context['model'].BulkUpload_Package

class StandingDataController(NgdsCrudController):
    """Controls CRUD API for StandingDataController"""
    def __init__(self, context):
        """Find the right model for this class"""
        self.model = context['model'].StandingData

class UserSearchController(NgdsCrudController):
    """Controls CRUD API for UserSearchController"""
    def __init__(self, context):
        """Find the right model for this class"""
        self.model = context['model'].UserSearch

class DocumentIndexController(NgdsCrudController):
    """Controls CRUD API for DocumentIndex"""
    def __init__(self, context):
        """Find the right model for this class"""
        self.model = context['model'].DocumentIndex
