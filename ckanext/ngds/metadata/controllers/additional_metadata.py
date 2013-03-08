from ckan.plugins.toolkit import toolkit
from ckanext.ngds.base.controllers.ngds_crud_controller import NgdsCrudController
from ckanext.ngds.metadata.model.additional_metadata import ResponsibleParty
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
    elif request_model == "AdditionalPackageMetadata":
        controller = AdditionalPackageMetadataController(context)
    elif request_model == "AdditionalResourceMetadata":
        controller = AdditionalResourceMetadataController(context)
    else:
        raise toolkit.ValidationError({}, "Please supply a 'model' attribute in the POST body. Value can be one of: ResponsibleParty, AdditionalPackageMetadata, AdditionalResourceMetadata")
    
    # execute method inspects POST body and runs the correct functions
    return controller.execute(data_dict)
    

class AdditionalResourceMetadataController(NgdsCrudController):
    """A class for controlling additional resource metadata RPC"""
    def __init__(self, context):
        """Find the right model for this class"""
        self.model = context['model'].AdditionalResourceMetadata        

class AdditionalPackageMetadataController(NgdsCrudController):
    """A class for controlling additional package metadata RPC"""
    def __init__(self, context):
        """Find the right model for this class"""
        self.model = context['model'].AdditionalPackageMetadata    
    
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
        
        user_list = []
        for user in query.all():
            result_dict = {}
            for k in ['id', 'name']:
                    result_dict[k] = getattr(user,k)

            user_list.append(result_dict)

        return user_list
    
    