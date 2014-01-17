''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''


from sqlalchemy import Column, Table, String, Text, Integer, types, ForeignKey
from sqlalchemy.orm import relationship

from ckan import model
from ckan.model import meta, Package

import logging
log = logging.getLogger(__name__)

contentmodels= []
usgin_url= None

checkfile_maxerror= 5
checkfile_checkheader= True
checkfile_checkoptionalfalse= False

class ContentModelRecord(object):
    """
    Class representing one ContentModel Record to be cached on the local node.
    """
    def __init__(self, package_id=None, **kwargs):
        self.identifier = kwargs.get("identifier", None)
        self.typename = kwargs.get("typename", None)

        self.status = kwargs.get("status", None)
        self.description = kwargs.get("description", None)
        self.title = kwargs.get("title", None)
        self.date_updated = kwargs.get("date_updated", None)
        self.discussion = kwargs.get("discussion", None)
        self.versions = kwargs.get("versions", None)
        self.uri = kwargs.get("uri", None)


class ContentModelVersion(object):
    """
    Class representing one ContentModel Record to be cached on the local node.
    """
    def __init__(self, package_id=None, **kwargs):
        self.uri = kwargs.get("uri", None)
        self.xsd_file_path = kwargs.get("xsd_file_path", None)
        self.version = kwargs.get("version", None)
        self.xls_file_path = kwargs.get("xls_file_path", None)
        self.date_created = kwargs.get("date_created", None)
        self.sample_wfs_request + kwargs.get("sample_wfs_request", None)


        
def define_tables():
    """
    Create in-memory representation of the tables, configure mappings to 
    python classes, and return the tables
    
    Table generation code is lifted from csw extension
    """
    contentmodel_record = Table(
        "contentmodel_record", meta.metadata,
        
        # core; nothing happens without these
        Column('identifier', String(256), primary_key=True),
        Column('typename', String(32),
               default='contentmodel:Record', nullable=False, index=True),
        
        Column('status', types.UnicodeText),
        Column('description', types.UnicodeText),
        Column('title', types.UnicodeText),
        Column('date_updated', types.DateTime),
        Column('discussion', types.UnicodeText), 
        # Column('versions', String(256), ForeignKey("contentmodelversion.uri")), 
        Column('uri', String(256))
    )
    
    contentmodel_version_record = Table(
        "contentmodel_version_record", meta.metadata,
        Column('typename', String(32),
               default='contentmodelversion:Record', nullable=False, index=True),
        Column('contentmodel_record', String(256), ForeignKey("contentmodel_record.identifier")), # Implicit Foreign Key to the content model
        Column("uri", String(256), primary_key=True),
        Column("xsd_file_path", String(256)),
        Column("version", String(32)),
        Column("xls_file_path", String(256)),
        Column("date_created", types.DateTime),
        Column("sample_wfs_request", String(256))
    )
    
    # Map the table to the class...
    meta.mapper(
        ContentModelRecord, 
        contentmodel_record
    )
    meta.mapper(
        ContentModelVersion, 
        contentmodel_version_record,
        properties={
            "contentmodel_record": relationship(ContentModelRecord)
        }
    )
    
    # put the ContentModelRecord class into CKAN model for later reference
    model.ContentModelRecord = ContentModelRecord
    model.ContentModelVersion = ContentModelVersion
    
    return contentmodel_record

def db_setup():
    """Create tables in the database"""
    # These tables will already be defined in memory if the csw plugin is enabled.
    #  IConfigurer will make a call to define_tables()
    contentmodel_record = meta.metadata.tables.get("contentmodel_record", None)
    
    if contentmodel_record == None:
        # The tables have not been defined. Its likely that the plugin is not enabled in the CKAN .ini file
        log.debug("Could not create contentmodel_record tables. Please make sure that you've added the csw plugin to your CKAN config .ini file.")
    else:    
        log.debug('contentmodel_record tables defined in memory')
    
    contentmodel_version_record = meta.metadata.tables.get("contentmodel_version_record", None)
    
    if contentmodel_version_record == None:
        # The tables have not been defined. Its likely that the plugin is not enabled in the CKAN .ini file
        log.debug("Could not create contentmodel_version_record tables. Please make sure that you've added the csw plugin to your CKAN config .ini file.")
    else:    
        log.debug('contentmodel_version_record tables defined in memory')
    
        # All right. Create the tables.
        from ckanext.ngds.base.commands.ngds_tables import create_tables
        create_tables([contentmodel_record], log)
        create_tables([contentmodel_version_record], log)