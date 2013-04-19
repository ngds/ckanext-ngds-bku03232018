import logging
#import pylons
#from sqlalchemy.exc import ProgrammingError

import ckan.plugins as p
import ckanext.ngds.contentmodel.logic.action as action
import ckanext.ngds.contentmodel.model.contentmodels as contentmodels
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
    p.implements(p.IConfigurable, inherit=True)
    p.implements(p.IActions)
    p.implements(p.IAuthFunctions)

    def configure(self, config):
        if "usgin_url" in config: 
            contentmodels.usgin_url= config["usgin_url"]
        else:
            contentmodels.usgin_url= "http://schemas.usgin.org/contentmodels.json"
        # Access the URL and fill the cache
        print "Caching Content Models from USGIN: " + contentmodels.usgin_url
        action.contentmodel_refreshCache(None, None)
        
        True_List = ["true", "1", "t", "y", "yes", "yeah", "yup", "certainly"]

        if "checkfile_maxerror" in config:
            try:
                checkfile_maxerror= config["checkfile_maxerror"]
                contentmodels.checkfile_maxerror = int(checkfile_maxerror)
            except:
                print "DON'T UNDERSTAND the 'checkfile_maxerror' in the development.ini, it is not an Integer"
        print "checkfile_maxerror", contentmodels.checkfile_maxerror

        if "checkfile_checkheader" in config:
            try:
                checkfile_checkheader= config["checkfile_checkheader"]
                if checkfile_checkheader in True_List:
                    contentmodels.checkfile_checkheader = True
                else:
                    contentmodels.checkfile_checkheader = False
            except:
                print "DON'T UNDERSTAND the 'checkfile_checkheader' in the development.ini, it is not a boolean string"
        print "checkfile_checkheader", contentmodels.checkfile_checkheader

        if "checkfile_checkoptionalfalse" in config:
            try:
                checkfile_checkoptionalfalse= config["checkfile_checkoptionalfalse"]
                if checkfile_checkoptionalfalse in True_List:
                    contentmodels.checkfile_checkoptionalfalse = True
                else:
                    contentmodels.checkfile_checkoptionalfalse = False
            except:
                print "DON'T UNDERSTAND the 'checkfile_checkoptionalfalse' in the development.ini, it is not a boolean string"
        print "checkfile_checkoptionalfalse", contentmodels.checkfile_checkoptionalfalse

    def get_actions(self):
        actions = {'contentmodel_refreshCache' : action.contentmodel_refreshCache, 'contentmodel_list' : action.contentmodel_list, 'contentmodel_list_short' : action.contentmodel_list_short, 'contentmodel_get': action.contentmodel_get, 'contentmodel_checkFile': action.contentmodel_checkFile}
        return actions

    def get_auth_functions(self):
        return {'contentmodel_refreshCache' : auth.datastore_create, 'contentmodel_list' : auth.datastore_create, 'contentmodel_checkFile' : auth.datastore_create}

