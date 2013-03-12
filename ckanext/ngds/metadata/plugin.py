from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IDatasetForm, IConfigurer, IActions, IRoutes
from ckanext.ngds.metadata.controllers.additional_metadata import dispatch
from ckanext.ngds.metadata.model.additional_metadata import define_tables
import os

class MetadataPlugin(SingletonPlugin):
    """The purpose of this plugin is to adjust the metadata content to conform to our standards"""
    
    implements(IConfigurer) # Allows access to configurations (like template locations)
    implements(IRoutes,inherit=True) 

    def update_config(self, config):
        """IConfigurable function. config is a dictionary of configuration parameters"""
        # Provides a point to do mappings from classes to database tables whenever CKAN is run
        define_tables()
        
        '''
        # First find the full path to my template directory
        here = os.path.dirname(__file__)
        template_dir = os.path.join(here, "templates") 
        
        # Now add that directory to the extra_template_paths, without removing the existing ones
        config['extra_template_paths'] = ','.join([template_dir, config.get('extra_template_paths', '')])   
        '''

    def before_map(self,map):
        map.connect("responsible_parties","/responsible_parties",controller="ckanext.ngds.metadata.controllers.additional_metadata:Responsible_Parties_UI",action="get_responsible_parties",conditions={"method":["GET"]})   
        map.connect("languages","/languages",controller="ckanext.ngds.metadata.controllers.additional_metadata:Languages_UI",action="get_languages",conditions={"method":["GET"]})   
        return map
    
    implements(IActions) # Allows us to build a URL and associated binding to a python function
    
    def get_actions(self):
        """IActions function. Should return a dict keys = function name and URL, value is the function to execute"""
        return {
            "additional_metadata": dispatch
        }
        
        
    '''
    implements(IDatasetForm) # Allows access to the forms that control user entry and mapping to DB
    
    def package_form(self):
        return 'package/new_package_form.html'

    def new_template(self):
        return 'package/new.html'

    def comments_template(self):
        return 'package/comments.html'

    def search_template(self):
        return 'package/search.html'

    def read_template(self):
        return 'package/read.html'

    def history_template(self):
        return 'package/history.html'
    
    def setup_template_variables(self, context, data_dict=None, package_type=None):
        pass
        
    def package_types(self):
        """
        Required IDatasetForm function. Sets the dataset type associated with your extension, and updates the
        routing so that datasets of this type can be found at the /<type> URL
        """
        return ['dataset'] # So I'm overriding what happens at /dataset
    
    def is_fallback(self):
        """
        Required IDatasetForm function. Kind of redundant with above -- if returns True, even when the return
        value of package_type is changed, going to /dataset/new will still use this extension's dataset form
        instead of CKAN's default.
        """
        return True
    
    def form_to_db_schema(self, package_type=None):
        from ckan.logic.schema import package_form_schema
        from ckan.lib.navl.validators import ignore_missing
        
        schema = package_form_schema()
        schema.update({
            'testy': [ignore_missing, unicode] 
        })
        return schema
        
    def db_to_form_schema(self, package_type=None):
        from ckan.logic.schema import package_form_schema
        from ckan.lib.navl.validators import ignore_missing, keep_extras
        
        schema = package_form_schema()
        schema.update({
            'testy': [ignore_missing, unicode]               
        })
        return schema
    '''