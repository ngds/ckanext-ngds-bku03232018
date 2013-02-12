from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer
from ckanext.ngds.csw.model.csw_records import define_tables

class CswPlugin(SingletonPlugin):
    """The purpose of this plugin is to add CSW support"""
    
    implements(IConfigurer) # Allows access to configurations (like template locations)
    
    def update_config(self, config):
        """IConfigurable function. config is a dictionary of configuration parameters"""
        # Provides a point to do mappings from classes to database tables whenever CKAN is run
        define_tables()