import urllib2, simplejson
import logging
import pylons
import ckan.logic as logic
import ckan.plugins as p
import sqlalchemy

from pylons import config

import ckanext.ngds.contentmodel.model.contentmodels


log = logging.getLogger(__name__)
_get_or_bust = logic.get_or_bust

@logic.side_effect_free
def contentmodel_refreshCache(context, data_dict):
    '''Refreshes the cache containing the NGDS content models from the USGIN Web Site

    This action contact the USGIN home page for content models 
    (http://schemas.usgin.org/models, http://schemas.usgin.org/contentmodels.json) and
    and downloads all content models from the site. It also refreshes a table that
    contains the status data of all content models.

    **Parameters:**
    None.
    
    **Results:**
    :returns: A status object (either success, or failed).
    :rtype: dictionary
    '''  
    remotefile = urllib2.urlopen(ckanext.ngds.contentmodel.model.contentmodels.usgin_url)
    ckanext.ngds.contentmodel.model.contentmodels.contentmodels = simplejson.load(remotefile)
    # return ckanext.ngds.contentmodel.model.contentmodels.contentmodels

@logic.side_effect_free
def contentmodel_list(context, data_dict):
    '''List all the cached Content Models on the CKAN node.
    **Parameters:**
    None.
    
    **Results:**
    :returns: The list of all available content models.
    :rtype: list
    '''
    return ckanext.ngds.contentmodel.model.contentmodels.contentmodels

@logic.side_effect_free
def contentmodel_list_short(context, data_dict):
    '''List all the cached Content Models on the CKAN node but abbreviate the returned result to
    show only the following dictionary entries per content model:
    - title
    - description
    - versions
       * uri
       * version
 
    An example output should look like this:
       [ { 'title': 'blabla', 'description': 'more bla', 
        'versions': [ {'uri': 'http://...', 'version': '1.5'}, {...} ], 
        'uri': 'http://...'},
      . . .
    ]  

    
    **Parameters:**
    None.
    
    **Results:**
    :returns: The list of all available content models.
    :rtype: list
    '''
    modelsshort= [] 
    for model in ckanext.ngds.contentmodel.model.contentmodels.contentmodels:
        m= {}
        m['title']= model['title']
        m['description']= model['description']
        versions= []
        for version in model['versions']:
            v= {}
            v['uri']= version['uri']
            v['version']= version['version']
            versions.append(v)
        m['versions']= versions
        m['uri']= model['uri']
        modelsshort.append(m)   

    return modelsshort

@logic.side_effect_free
def contentmodel_get(context, data_dict):
    '''Returns the information about a certain content model.
    
    This action returns detailed information about a specific content model.
    **Parameters:**
    :param cm_uri: uri of the content model.
    :type cm_uri: string

    :param cm_version: version of the content model.
    :type cm_version: string
    '''
    cm_uri = _get_or_bust(data_dict, 'cm_uri')
    cm_version= _get_or_bust(data_dict, 'cm_version')
    
    schema= [ rec for rec in ckanext.ngds.contentmodel.model.contentmodels.contentmodels
              if rec['uri'] == cm_uri ]
    
    if schema.__len__() != 1:
        raise p.toolkit.ObjectNotFound(p.toolkit._(
            'Schema with the URI "{0}" was not found.'.format(cm_uri)
        ))
    
    # schema is a list with a single entry
    schema_versions= schema[0]['versions']
    
    version= [ rec for rec in schema_versions if rec['version'] == cm_version]
    if version.__len__() != 1:
        raise p.toolkit.ObjectNotFound(p.toolkit._(
            'Schema version with the URI "{0}" and version {1} was not found.'.format(cm_uri, cm_version)
        ))
        
    # version is again a list with a single entry
    return version[0]

@logic.side_effect_free
def contentmodel_checkFile(context, data_dict):
    '''Refresh the cache of Content Models on the CKAN node.
    **Parameters:**
    None.
    
    **Results:**
    :returns: The list of all available content models.
    :rtype: vector
    '''
    if 'id' in data_dict:
        data_dict['resource_id'] = data_dict['id']
    res_id = _get_or_bust(data_dict, 'resource_id')
       
    data_dict['connection_url'] = pylons.config['ckan.datastore.write_url']


