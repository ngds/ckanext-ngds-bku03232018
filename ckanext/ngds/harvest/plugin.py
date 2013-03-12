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