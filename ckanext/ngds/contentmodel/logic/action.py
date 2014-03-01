''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

import urllib2, simplejson
import logging
import ckan.logic as logic
import ckan.plugins as p
import usginmodels

from ckan.plugins import toolkit

import csv
import ckanext.ngds.contentmodel.model.contentmodels
import ckanext.ngds.contentmodel.model.usgin_ogc as usgin_ogc

from ContentModel_Utilities import *

log = logging.getLogger(__name__)
_get_or_bust = logic.get_or_bust

CONTENTMODELS = None

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

    if ckanext.ngds.contentmodel.model.contentmodels.usgin_url is None:
        ckanext.ngds.contentmodel.model.contentmodels.usgin_url = "http://schemas.usgin.org/contentmodels.json"
    remotefile = urllib2.urlopen(ckanext.ngds.contentmodel.model.contentmodels.usgin_url)
    CONTENTMODELS = simplejson.load(remotefile)
    ckanext.ngds.contentmodel.model.contentmodels.contentmodels = CONTENTMODELS

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
    if len(ckanext.ngds.contentmodel.model.contentmodels.contentmodels) == 0: contentmodel_refreshCache({}, {})
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
    if len(ckanext.ngds.contentmodel.model.contentmodels.contentmodels) == 0: contentmodel_refreshCache({}, {})
    for model in ckanext.ngds.contentmodel.model.contentmodels.contentmodels:
        m= {}
        m['title']= model['title']
        m['description']= model['description']
        versions= []
        for version in model['versions']:
            v= {}
            v['uri']= version['uri']
            v['version']= version['version']
            v['layers'] = version['layers_info']
            versions.append(v)
        m['versions']= versions
        m['uri']= model['uri']
        m['label'] = model['label']
        modelsshort.append(m)   

    # print modelsshort
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
    schema_label = schema[0]['label']
    schema_versions= schema[0]['versions']
    
    version= [ rec for rec in schema_versions if rec['version'] == cm_version]
    if version.__len__() != 1:
        raise p.toolkit.ObjectNotFound(p.toolkit._(
            'Schema version with the URI "{0}" and version {1} was not found.'.format(cm_uri, cm_version)
        ))
        
    # version is again a list with a single entry
    return {'label': schema_label, 'version': version[0]}

@logic.side_effect_free
def contentmodel_checkFile(context, data_dict):
    '''Check whether the given csv file follows the specified content model.
    
    This action returns detailed description of inconsistent cells.
    **Parameters:**
    :param cm_uri: uri of the content model.
    :type cm_uri: string

    :param cm_version: version of the content model.
    :type cm_version: string

    :param cm_resource_url: the URL to the resource
    :type cm_resource_url: string
    
    **Results:**
    :returns: A status object (either success, or failed).
    :rtype: dictionary
    '''


    cm_resource_url = _get_or_bust(data_dict, 'cm_resource_url')
    modified_resource_url = cm_resource_url.replace("%3A", ":")
    truncated_url = modified_resource_url.split("/storage/f/")[1]
    csv_filename_withfile = get_url_for_file(truncated_url)
    validation_msg = []
    
    if csv_filename_withfile is None:
        msg = toolkit._("Can't find the full path of the resources from %s" % cm_resource_url)
        validation_msg.append({'row':0, 'col':0, 'errorTYpe': 'systemError', 'message':msg})
    else:
        log.info("filename full path: %s " % csv_filename_withfile)

    this_layer = _get_or_bust(data_dict, 'cm_layer')
    this_uri = _get_or_bust(data_dict, 'cm_uri')
    this_version_uri = _get_or_bust(data_dict, 'cm_version_url')

    if this_layer.lower() and this_uri.lower() and this_version_uri.lower() == 'none':
        log.debug("tier 2 data model/version/layer are none")
        return {"valid": True, "messages": "Okay"}
    else:
        log.debug("about to start schema reading")
        user_schema = contentmodel_get(context, data_dict)
        # print user_schema
        fieldModelList = []
        field_info_list = user_schema['version']['layers_info']

        for field_info in field_info_list[this_layer]:
            if ((field_info['name'] is None) and ((len(field_info['type'])==0) or (field_info['type'].isspace()))):
                log.debug("found a undefined field: %s" % str(field_info))
                continue
            else:
                fieldModelList.append(ContentModel_FieldInfoCell(field_info['optional'], field_info['type'], field_info['name'], field_info['description']))

        log.debug(fieldModelList)
        log.debug("finish schema reading, find %s field information" % str(len(fieldModelList)))

        if len(validation_msg) == 0:
            try:
                csv_filename = csv_filename_withfile.split("file://")[1]
                this_csv = open(csv_filename, 'rbU')

                valid, errors, dataCorrected, long_fields, srs = usginmodels.validate_file(
                    this_csv,
                    this_version_uri,
                    this_layer
                )

                if valid:
                    pass
                else:
                    validation_msg.append({'valid': False})
            except:
                validation_msg.append({'valid': False})

    log.debug(validation_msg)
    # print 'JSON:', json.dumps({"valid": "false", "messages": validation_msg})
    if len(validation_msg) == 0:
        return {"valid": True, "messages": "Okay"}
    else:
        return {"valid": False, "messages": validation_msg}

@logic.side_effect_free
def contentmodel_checkBulkFile(context,cm_dict):
    '''Check whether the given content model is a valid one.

    **Parameters:**
    :param cm_uri: uri of the content model.
    :type cm_uri: string

    :param cm_version: version of the content model.
    :type cm_version: string

    :param cm_resource_url: the URL to the resource
    :type cm_resource_url: string
    
    **Results:**
    :returns: A status object (either success, or failed).
    :rtype: dictionary
    '''

    print "Context: ", context

    title = cm_dict.get('content_model')
    version = cm_dict.get('version')

    schema = [rec for rec in ckanext.ngds.contentmodel.model.contentmodels.contentmodels if rec['title'].strip().lower() == str(title).strip().lower()]

    if schema.__len__() != 1:
        raise Exception(toolkit._("Invalid content model: %s") % title)

    # schema is a list with a single entry
    content_model = schema[0]

    versionExists = False

    for c_version in content_model['versions']:
        if c_version['version'] == str(version):
            versionExists = True
            version_uri = c_version['uri']

    if not versionExists:
        raise Exception(toolkit._("Invalid content model version. Content Model: %s ,version: %s") % (title,version))

    return content_model['uri'], version_uri


def create_contentmodel_table(context, data_dict):
    """
    This will create a table for a specific content model and version. Created table will be used for consolidating
    all content model specific data so that further representations can be done.
    """

    cm_uri = _get_or_bust(data_dict, 'cm_uri')
    cm_version = _get_or_bust(data_dict, 'cm_version')
    cm_resource_url = _get_or_bust(data_dict, 'cm_resource_url')

    try:

        cm_schema = contentmodel_get(context, data_dict)
    except Exception as ex:
        print ex

    table_name = get_contentmodel_name(cm_schema)

    field_info_list = cm_schema['field_info']

    from sqlalchemy import types, Column, Table, MetaData
    from ckanext.ngds.env import DataStoreSession

    session = DataStoreSession()
    metadata = MetaData(bind=session.bind)

    table = Table(table_name, metadata,
                  Column('id', types.Integer, primary_key=True),
                  *(Column(field_info.get('name'), get_sqlalchemy_datatype(field_info.get('type'))) for field_info in field_info_list if field_info.get('name')))

    if not table.exists():
        table.create()

    with open(cm_resource_url) as f:
        csv_content = csv.DictReader(f, delimiter=',')

        for record in csv_content:
            # insert data into the table
            record = {k.strip(): v if v else None for k, v in record.items()}
            table.insert().values(**record).execute()


def get_sqlalchemy_datatype(cm_datatype):
    """
    Returns the sqlalchemy datatype for a content model field based on data type defined in the content model spec.
    """
    from sqlalchemy import types
    data_type = {
        'int':types.Integer,
        'string':types.String,
        'text':types.UnicodeText,
        'double':types.Numeric,
        'date':types.DateTime
    }

    sqlalchemyType = types.UnicodeText

    if cm_datatype and cm_datatype in data_type:
        sqlalchemyType = data_type.get(cm_datatype)

    return sqlalchemyType

def get_contentmodel_name(cm_schema):
    """
    Gets the content model name based on the schema. Replaces the spaces in the content model name so that it can be
    used as a table name.
    """
    cm_name = "test"

    uri = cm_schema['uri']

    def find(str, ch):
        return [i for i, ltr in enumerate(str) if ltr == ch]

    pos = find(uri, '/')

    model_name_pos = pos[len(pos)-2]

    version_pos = pos[len(pos)-1]

    model_name = uri[model_name_pos+1:]

    chars = [',', '!', '.', '-', '/']

    import re
    cm_name = re.sub('[%s]' % ''.join(chars), '_', model_name)

    return cm_name

@logic.side_effect_free
def publish_usgin_layer(context, data_dict):
    usgin = usgin_ogc.EnforceUSGIN(context, data_dict)
    usgin.publish_ogc()
    return