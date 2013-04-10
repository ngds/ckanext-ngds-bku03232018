import logging
import pylons
import ckan.logic as logic
import ckan.plugins as p
import sqlalchemy

from pylons import config

log = logging.getLogger(__name__)
_get_or_bust = logic.get_or_bust

def contentmodel_refreshCache(context, data_dict):
    '''Refreshes the cache containing the NGDS content models from the USGIN Web Site

    This action contact the USGIN home page for content models 
    (http://schemas.usgin.org/models, http://schemas.usgin.org/contentmodels.json) and
    and downloads all content models from the site. It also refreshes a table that
    contains the status data of all content models.
    
    **Results:**

    :returns: A status object (either success, or failed).
    :rtype: dictionary
    '''
    
    if 'id' in data_dict:
        data_dict['resource_id'] = data_dict['id']
    res_id = _get_or_bust(data_dict, 'resource_id')
       
    data_dict['connection_url'] = pylons.config['ckan.datastore.write_url']

    



def contentmodel_list(context, data_dict):
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


