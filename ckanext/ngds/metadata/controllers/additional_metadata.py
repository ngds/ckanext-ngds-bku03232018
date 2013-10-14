''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

from ckan.plugins.toolkit import toolkit
from ckanext.ngds.base.controllers.ngds_crud_controller import NgdsCrudController
from ckanext.ngds.metadata.model.additional_metadata import ResponsibleParty, Language
from pylons import c, request, response
import ckan.lib.base as base
import ckan.lib.jsonp as jsonp

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
        
        responsible_parties = []
        for responsible_party in query.all():
            result_dict = {}
            for k in ['id', 'name','email']:
                    result_dict[k] = getattr(responsible_party,k)

            responsible_parties.append(result_dict)

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
