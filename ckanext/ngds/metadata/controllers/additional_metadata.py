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
from ckanext.ngds.metadata.model.additional_metadata import ResponsibleParty, Language
from pylons import c, request, response
import ckan.lib.base as base
import ckan.lib.jsonp as jsonp
import json

def dispatch(context, data_dict):
    """
    Send the action request to the correct place, based on the POST body
    
    Body should contain JSON data as follows:
    {
      "model": One of ResponsibleParty, AdditionalPackageMetadata, AdditionalResourceMetadata
      "process": One of "create", "read", "update", "delete"
      "data": An object containing the data to act on
    }
    
    Requests are inspected and passed on to model-specific controllers, defined below
    
    """
    
    # Determine the correct controller by inspecting the data_dict
    request_model = data_dict.get("model", None)
    controller = None
    if request_model == "ResponsibleParty":
        controller = ResponsiblePartyController(context)
    else:
        raise toolkit.ValidationError({}, "Please supply a 'model' attribute in the POST body. Value can be one of: ResponsibleParty, AdditionalPackageMetadata, AdditionalResourceMetadata")
    
    # execute method inspects POST body and runs the correct functions
    return controller.execute(data_dict)
    
class ResponsiblePartyController(NgdsCrudController):
    """A class for controlling responsible party RPC"""
    def __init__(self, context):
        """Find the right model for this class"""
        self.model = context['model'].ResponsibleParty


class Responsible_Parties_UI(base.BaseController):
    @jsonp.jsonpify
    def get_responsible_parties(self):
        q = request.params.get('q', '')
        query =ResponsibleParty.search(q).limit(10)
        
        responsible_parties = {"ResultSet":{"Result":[]}}
        for responsible_party in query.all():
            result_dict = {}
            name = getattr(responsible_party,"name")
            email = getattr(responsible_party,"email")
            result_dict["name"] = name
            result_dict["value"] = json.dumps({"name":name,"email":email})
            responsible_parties["ResultSet"]["Result"].append(result_dict)

        return responsible_parties
    
class Languages_UI(base.BaseController):
    @jsonp.jsonpify
    def get_languages(self):
        q = request.params.get('q', '')
        query =Language.search(q).limit(10)
        
        languages = []
        for language in query.all():
            result_dict = {}
            for k in ['id', 'name','code']:
                    result_dict[k] = getattr(language,k)

            languages.append(result_dict)

        return languages    
