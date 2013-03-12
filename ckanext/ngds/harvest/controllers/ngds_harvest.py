from ckan.plugins.toolkit import toolkit
from ckanext.ngds.base.controllers.ngds_crud_controller import NgdsCrudController

def dispatch(context, data_dict):
    """
    Send the action request to the correct place, based on the POST body
    
    Body should contain JSON data as follows:
    {
      "model": One of HarvestNode, HarvestedRecord
      "process": One of "create", "read", "update", "delete"
      "data": An object containing the data to act on
    }
    
    Requests are inspected and passed on to model-specific controllers, defined below
    
    """
    
    # Determine the correct controller by inspecting the data_dict
    request_model = data_dict.get("model", None)
    controller = None
    if request_model == "HarvestNode":
        controller = HarvestNodeController(context)
    elif request_model == "HarvestedRecord":
        controller = HarvestedRecordController(context)
    else:
        raise toolkit.ValidationError({}, "Please supply a 'model' attribute in the POST body. Value can be one of: HarvestNode, HarvestedRecord")
    
    # execute method inspects POST body and runs the correct functions
    return controller.execute(data_dict)

class HarvestNodeController(NgdsCrudController):
    """Controls CRUD API for HarvestNodes"""
    def __init__(self, context):
        """Find the right model for this class"""
        self.model = context['model'].HarvestNode
        
class HarvestedRecordController(NgdsCrudController):
    """Controls CRUD API for HarvestNodes"""
    def __init__(self, context):
        """Find the right model for this class"""
        self.model = context['model'].HarvestedRecord
        
def do_harvest(context, data_dict):
    """
    Perform a harvest
    
    POST body should identify the ID of a HarvestNode
    { "id": "harvest-node-id" }
    
    """
    the_id = data_dict.get("id", None)
    if the_id == None:
        raise toolkit.ValidationError({}, "Please supply the ID of a HarvestNode that you want to harvest")
    else:
        node = context['model'].HarvestNode.by_id(the_id)
        node.do_harvest()
    
        