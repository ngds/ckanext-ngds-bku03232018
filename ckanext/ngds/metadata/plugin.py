from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer, IActions, IRoutes,IFacets,IPackageController
from ckanext.ngds.metadata.controllers.additional_metadata import dispatch
from ckanext.ngds.metadata.controllers.transaction_data import dispatch as trans_dispatch

from ckan import model

import ckan.plugins as p
_ = p.toolkit._

try:
    from collections import OrderedDict # 2.7
except ImportError:
    from sqlalchemy.util import OrderedDict

from pylons import config   
from ckan.lib.base import (model,abort, h, g, c)



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


    '''
    The following should go into ngdsui plugin. For now to test with CKAN UI facets are coded here.
    '''        

    implements(IFacets,inherit=True)
    def dataset_facets(self,facets_dict,dataset_type):

        try:
            if g.loaded_facets:
                return g.loaded_facets
        except AttributeError:
            print "facets are yet to be loaded from the config."

        facets_config_path = config.get('ngds.facets_config')

        #facets_dict = OrderedDict([('private', _('Public/ Private')),('tags', _('Tags')),('res_format', _('Formats')),('status', _('Status')),('author', _('Author')),])

        if facets_config_path:
            loaded_facets = self.load_facets(facets_config_path=facets_config_path)
        
        if loaded_facets:
            g.loaded_facets = loaded_facets
            facets_dict = loaded_facets

        #print "facets_dict: ",facets_dict

        return  facets_dict

    def load_facets(self,facets_config_path=None):
        '''
        This Method loads the given facets config file and constructs the facets structure to be used.
        '''

        with open(facets_config_path, 'r') as json_file:
            import json
            from pprint import pprint
            json_data = json.load(json_file)

            g.facet_json_data = json_data

            #facets_dict =OrderedDict()
            facets_list = []

            for facet in json_data:
                facets_list = self.read_facet(facet,facets_list)

        if facets_list:
            return OrderedDict(facets_list)
        else:
            return None

    def read_facet(self,facet_config,facet_list):

        if facet_config.get("metadatafield") :
            facet_list.append((facet_config['metadatafield'],_(facet_config.get("facet"))))

        if facet_config.get("subfacet"):
            for subfacet in facet_config.get("subfacet"):
                facet_list = self.read_facet(subfacet,facet_list)

        return facet_list


    implements(IPackageController,inherit=True)
    def after_search(self,search_results, search_params):

        try:
            import json
            if g.facet_json_data:
                print "global value is there..."
        except AttributeError:
            print "Facet json config is not available. Returning the default facets."
        
        #print "search_results: ", json.dumps(search_results)

        return search_results