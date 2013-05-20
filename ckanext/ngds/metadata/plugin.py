from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer, IActions, IRoutes,IFacets,IPackageController,ITemplateHelpers
from ckanext.ngds.metadata.controllers.additional_metadata import dispatch
from ckanext.ngds.metadata.controllers.transaction_data import dispatch as trans_dispatch

from ckan import model


class MetadataPlugin(SingletonPlugin):
    """The purpose of this plugin is to adjust the metadata content to conform to our standards"""
    
    implements(IConfigurer) # Allows access to configurations (like template locations)
    implements(IRoutes,inherit=True) 

    def update_config(self, config):
        """IConfigurable function. config is a dictionary of configuration parameters"""
        # Provides a point to do mappings from classes to database tables whenever CKAN is run

        if not hasattr(model, "ResponsibleParty"):
            from ckanext.ngds.metadata.model.additional_metadata import define_tables
            define_tables()

            from ckanext.ngds.metadata.model.transaction_tables import define_tables as trans_define_tables
            trans_define_tables()            
        
            # Put IsoPackage into ckan.model for ease of access later
            from ckanext.ngds.metadata.model.iso_package import IsoPackage
            model.IsoPackage = IsoPackage
        
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
            "additional_metadata": dispatch,
            "transaction_data": trans_dispatch
        }