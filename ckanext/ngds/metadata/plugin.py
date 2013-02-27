from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer, IActions
from ckanext.ngds.metadata.controllers.additional_metadata import dispatch

class MetadataPlugin(SingletonPlugin):
    """The purpose of this plugin is to adjust the metadata content to conform to our standards"""
    
    implements(IConfigurer) # Allows access to configurations (like template locations)
    
    def update_config(self, config):
        """IConfigurable function. config is a dictionary of configuration parameters"""
        # Provides a point to do mappings from classes to database tables whenever CKAN is run
        from ckanext.ngds.metadata.model.additional_metadata import define_tables
        define_tables()
        
        # Put IsoPackage into ckan.model for ease of access later
        from ckan import model
        from ckanext.ngds.metadata.model.iso_package import IsoPackage
        model.IsoPackage = IsoPackage
        
    implements(IActions) # Allows us to build a URL and associated binding to a python function
    
    def get_actions(self):
        """IActions function. Should return a dict keys = function name and URL, value is the function to execute"""
        return {
            "additional_metadata": dispatch
        }
        
    