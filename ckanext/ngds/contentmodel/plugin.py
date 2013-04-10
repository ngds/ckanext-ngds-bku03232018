import logging
#import pylons
#from sqlalchemy.exc import ProgrammingError

import ckan.plugins as p
import ckanext.ngds.contentmodel.logic.action as action
import ckanext.datastore.logic.auth as auth
#import ckanext.datastore.db as db
#from ckanext.datastore.plugin import DatastoreException
import ckan.logic as logic
#import ckan.model as model

log = logging.getLogger(__name__)
_get_or_bust = logic.get_or_bust


# We use this one from Datastore
#class DatastoreException(Exception):
#    pass


class ContentModelPlugin(p.SingletonPlugin):
    '''
    Content Model plugin.
    
    This plugin provides actions to "manage and use content models". Specifically the following 
    actions will be provided:  
    1. refreshCache: This function updates the local cache of the repository. When the function
                     completed all Content Models are stored locally.
    2. listModels:   This function returns a list of all content models currently available. The 
                     data is returned as a JSON object.
    3. checkFile:    This function checks a file against a content model. It will return a JSON
                     object with information about the success or failure of the operation.
                      
    '''
    # p.implements(p.IConfigurable, inherit=True)
    p.implements(p.IActions)
    p.implements(p.IAuthFunctions)

    def get_actions(self):
        actions = {'contentmodel_refreshCache' : action.contentmodel_refreshCache, 'contentmodel_refreshCache' : action.contentmodel_list, 'contentmodel_checkFile': action.contentmodel_checkFile}
        return actions

    def get_auth_functions(self):
        return {'contentmodel_refreshCache' : auth.datastore_create, 'contentmodel_list' : auth.datastore_create, 'contentmodel_checkFile' : auth.datastore_create}

