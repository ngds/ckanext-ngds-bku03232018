from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IDatasetForm, IConfigurer, IActions
from ckanext.ngds.harvest.model.harvest_node import define_tables

class NgdsHarvestPlugin(SingletonPlugin):
    """Control harvesting operations"""
    
    implements(IConfigurer) # Allows access to configurations (like template locations)
    
    def update_config(self, config):
        """IConfigurable function. config is a dictionary of configuration parameters"""
        # Provides a point to do mappings from classes to database tables whenever CKAN is run
        define_tables()