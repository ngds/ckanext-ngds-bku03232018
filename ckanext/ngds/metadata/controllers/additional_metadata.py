from ckan.plugins.toolkit import toolkit
from ckanext.ngds.base.controllers.ngds_crud_controller import NgdsCrudController

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
    
    