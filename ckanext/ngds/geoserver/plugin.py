import logging
import pylons
from sqlalchemy.exc import ProgrammingError

import ckan.plugins as p
import ckanext.ngds.geoserver.logic.action as action
import ckanext.datastore.logic.auth as auth
import ckanext.datastore.db as db
from ckanext.datastore.plugin import DatastoreException
import ckan.logic as logic
import ckan.model as model

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
        actions = {'datastore_spatialize' : action.datastore_spatialize}
        return actions

    def get_auth_functions(self):
        return {'datastore_spatialize' : auth.datastore_create}

