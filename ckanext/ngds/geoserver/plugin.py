import logging

import ckan.plugins as p
from ckan.plugins import ITemplateHelpers, IRoutes, IResourcePreview
import ckanext.ngds.geoserver.logic.action as action
import ckanext.ngds.geoserver.model.GMLtoReclineJSON as recline
import ckanext.datastore.logic.auth as auth
import ckan.logic as logic
import ckanext.ngds.geoserver.misc.helpers as helpers

log = logging.getLogger(__name__)
_get_or_bust = logic.get_or_bust


# We use this one from Datastore
#class DatastoreException(Exception):
#    pass


class GeoserverPlugin(p.SingletonPlugin):
    '''
    Geoserver plugin.
    
    This plugin provides actions to "spatialize" tables in the datastore and to connect them with the Geoserver. Spatialize 
    means:
    1. Create an additional column of type (PostGIS) point
    2. Update the column with values calulated from already existing latitude/ longitude columns
    
    Connect to Geoserver means:
    1. Create a select statement
    2. Use the geoserver API to create a new layer using that select statement 
     
    '''
    # p.implements(p.IConfigurable, inherit=True)
    p.implements(p.IActions)
    p.implements(p.IAuthFunctions)

    def get_actions(self):
        '''
        actions = {'datastore_spatialize' : action.datastore_spatialize,
                   'datastore_expose_as_layer': action.datastore_expose_as_layer,
                   'datastore_is_spatialized' : action.datastore_is_spatialized,
                   'datastore_is_exposed_as_layer' : action.datastore_is_exposed_as_layer,
                   'datastore_remove_exposed_layer' : action.datastore_remove_exposed_layer,
                   'datastore_remove_all_exposed_layers' :action.datastore_remove_all_exposed_layers,
                   'datastore_list_exposed_layers' : action.datastore_list_exposed_layers,
                   'geoserver_create_workspace' : action.geoserver_create_workspace,
                   'geoserver_delete_workspace' : action.geoserver_delete_workspace,
                   'geoserver_create_store' : action.geoserver_create_store,
                   'geoserver_delete_store' : action.geoserver_delete_store,
                   'test':a.test }
        '''

        actions = {
           'geoserver_publish_layer':action.publish,
           'geoserver_layer_exists':action.layer_exists,
           'geoserver_unpublish_layer':action.unpublish,
        }
        
        return actions

    def get_auth_functions(self):
        functions =  {'datastore_spatialize' : auth.datastore_create, 
                'datastore_expose_as_layer' : auth.datastore_create,
                'datastore_is_spatialized' : auth.datastore_search,
                'datastore_is_exposed_as_layer' : auth.datastore_search,
                'datastore_remove_exposed_layer' : auth.datastore_delete,
                'datastore_remove_all_exposed_layers' :auth.datastore_delete,
                'datastore_list_exposed_layers' : auth.datastore_search,
                'geoserver_create_workspace' : auth.datastore_create,
                'geoserver_delete_workspace' : auth.datastore_delete,
                'geoserver_create_store' : auth.datastore_create,
                'geoserver_delete_store' : auth.datastore_delete,}
        
        return functions

    p.implements(ITemplateHelpers,inherit=True)
    def get_helpers(self):
      return {
        'is_spatialized':helpers.is_spatialized,
      }

    p.implements(IRoutes,inherit=True)
    def before_map(self,map):
      map.connect('spatialize','/ngds/publish_ogc',controller="ckanext.ngds.geoserver.controllers.ogc:OGCController",action="publish_ogc",conditions={"method":["POST"]})
      map.connect('publish_layer','/ngds/publish_layer',controller="ckanext.ngds.geoserver.controllers.ogc:OGCController",action="publish_layer",conditions={"method":["POST"]})

      return map

    # Start WFS preview plugin

    p.implements(p.IConfigurer, inherit=True)

    # Add new resource containing libraries, scripts, etc. to the global config
    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'geo-recline/theme/templates')
        p.toolkit.add_resource('geo-recline/theme/public', 'geo-reclinepreview')

    p.implements(IResourcePreview)

    # If the resource protocol is a WFS, then we can preview it
    def can_preview(self, data_dict):
        if data_dict.get("resource", {}).get("protocol", {}) == "OGC:WFS":
            return True

    # Get the GML service for our resource and parse it into a JSON object
    # that is compatible with recline.  Bind that JSON object to the
    # CKAN resource in order to pass it client-side.
    def setup_template_variables(self, context, data_dict):
        armchair = recline.GMLtoReclineJS()
        reclineJSON = armchair.MakeReclineJSON(data_dict)
        p.toolkit.c.resource["reclineJSON"] = reclineJSON

    # Render the jinja2 template which builds the recline preview
    def preview_template(self, context, data_dict):
        template = "wfs_preview_template.html"
        return template