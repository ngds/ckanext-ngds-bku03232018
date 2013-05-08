import logging
import pylons
from sqlalchemy.exc import ProgrammingError

import ckan.plugins as p
from ckan.plugins import ITemplateHelpers
import ckanext.ngds.geoserver.logic.action as action
import ckanext.datastore.logic.auth as auth
import ckanext.datastore.db as db
from ckanext.datastore.plugin import DatastoreException
import ckan.logic as logic
import ckan.model as model
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
                   'geoserver_delete_store' : action.geoserver_delete_store }
        
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
                'geoserver_delete_store' : auth.datastore_delete}
        
        return functions

    p.implements(ITemplateHelpers,inherit=True)
    def get_helpers(self):
      return {
        'is_spatialized':helpers.is_spatialized,
      }