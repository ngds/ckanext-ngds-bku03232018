import urllib2, simplejson
import logging
import pylons
import ckan.logic as logic
import ckan.plugins as p
import sqlalchemy

from pylons import config

import csv
import ckanext.ngds.contentmodel.model.contentmodels

from ContentModel_Utilities   import *


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
    '''Check whether the given csv file follows the specified content model.
    
    This action returns detailed description of inconsistent cells.
    **Parameters:**
    :param cm_uri: uri of the content model.
    :type cm_uri: string

    :param cm_version: version of the content model.
    :type cm_version: string

    :param csvfile: full path of a uploaded csv file
    :type csvfile: string
    
    **Results:**
    :returns: A status object (either success, or failed).
    :rtype: dictionary
    '''
    cm_uri     = _get_or_bust(data_dict, 'cm_uri')
    cm_version = _get_or_bust(data_dict, 'cm_version')
    csv_filename = _get_or_bust(data_dict, 'csvfile')
    
    validation_msg = []
    
    print "about to start schema reading"
    user_schema = contentmodel_get(context, data_dict)
    # print user_schema
    fieldModelList = []
    field_info_list = user_schema['field_info']
    for field_info in field_info_list:
        if ((field_info['name'] is None) and ((len(field_info['type'])==0) or (field_info['type'].isspace()))):
            print "found a undefined field: " + str(field_info)  
            continue
        else: 
            fieldModelList.append(ContentModel_FieldInfoCell(field_info['optional'], field_info['type'], field_info['name'], field_info['description']))
    print fieldModelList
    print "finish schema reading, find " + str(len(fieldModelList)) + " field information"  
    
    print "about to start CSV reading"
    dataHeaderList = []
    dataListList = []
    try:
        csv_reader = csv.reader(open(csv_filename, "rb"))
        header = csv_reader.next()
        dataHeaderList = [x.strip() for x in header]
        
        for row in csv_reader:
            new_row = [x.strip() for x in row]
            dataListList.append(new_row)
    except csv.Error as e:
        msg = "csv.Error file %s, line %d: %s" %(csv_filename, csv_reader.line_num, e)
        validation_msg.append(msg)
    except IOError as e:
        msg = "IOError file %s, %s" %(csv_filename, e)
        validation_msg.append(msg)
    print "about to finish CSV reading"

    if len(validation_msg) == 0:
        validation_existence_messages = validate_existence(fieldModelList, dataHeaderList, dataListList)
        if len(validation_existence_messages) > 0:
            validation_msg.extend(validation_existence_messages)
        
        validation_numericType_messages = validate_numericType(fieldModelList, dataHeaderList, dataListList)
        if len(validation_numericType_messages) > 0:
            validation_msg.extend(validation_numericType_messages)
        
        print "validation detailed error message"
        print validation_msg

    if len(validation_msg) == 0:
        return {"valid": "true", "message": "ok."}
    else:
        return {"valid": "false", "message": validation_msg}
