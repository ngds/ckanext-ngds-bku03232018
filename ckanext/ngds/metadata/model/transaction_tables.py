"""
Contains models for the transaction tables used part of ngds.

"""

from ckan import model


from ckan.model import meta

from sqlalchemy import types, Column, Table, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql.expression import or_ 
from sqlalchemy.sql import func

from sqlalchemy import types, Column, Table
from sqlalchemy.orm import validates

import datetime

from pylons import config

import csv
import logging
log = logging.getLogger(__name__)

from ckanext.ngds.base.model.ngds_db_object import NgdsDataObject
        
class BulkUpload(NgdsDataObject):
    """
    A BulkUpload represents the details of a bulk uploaded dataset and status of the processing.
    """
    
    def __init__(self, **kwargs):
        self.data_file = kwargs.get('data_file', None)
        self.resources = kwargs.get('resources', None)
        self.path = kwargs.get('path', None)
        self.status = kwargs.get('status', None)
        self.comments = kwargs.get('comments', None)
        self.uploaded_by = kwargs.get('uploaded_by', None)
        
    @classmethod
    def search(cls, querystr, sqlalchemy_query=None):
        '''Search name, fullname, email and openid. '''
        if sqlalchemy_query is None:
            query = meta.Session.query(cls)
        else:
            query = sqlalchemy_query

        query = query.filter(cls.status == querystr)
        return query
    
    @classmethod
    def by_data_file(cls, querystr):
        query = meta.Session.query(cls).filter(cls.data_file == querystr)
        member = query.first()        
        return member


    @classmethod
    def get(cls, reference):
        '''Returns a bulk upload record referenced by its id or name.'''
        query = meta.Session.query(cls).filter(cls.id == reference)
        member = query.first()
        if member is None:
            member = cls.by_data_file(reference)
        return member

class StandingData(NgdsDataObject):

    def __init__(self, **kwargs):
        self.description = kwargs.get('description', None)
        self.code = kwargs.get('code', None)
        self.data_type = kwargs.get('data_type', None)    

    @classmethod
    def validate(cls,data_type,sdvalue):
        """ This method validates whether given SD value is present in the model or not. 
        If exists returns SD description otherwise None """

        print "Data type:%s SD Value: %s" % (data_type,sdvalue)

        query = meta.Session.query(cls).filter(cls.data_type == data_type)
        query = query.filter(func.lower(cls.description) == sdvalue.lower())
        member = query.first()        
        if member is None:
            return None
        else:
            return member.description


def define_tables():
    """Create the in-memory represenatation of tables, and map those tables to classes defined above"""
    
    # First define the three tables
    bulkupload = Table(
        "bulk_upload",
        meta.metadata,
        Column("id", types.Integer, primary_key=True),
        Column("data_file", types.UnicodeText),
        Column("resources", types.UnicodeText),
        Column("path", types.UnicodeText),
        Column("status", types.UnicodeText),
        Column("comments", types.UnicodeText),
        Column("uploaded_by", types.UnicodeText, ForeignKey("user.id")),
        Column("uploaded_date", types.DateTime, default=datetime.datetime.now),
        Column('last_updated', types.DateTime, default=datetime.datetime.now),
    )

    standingdata = Table(
        "standing_data",
        meta.metadata,
        Column("id", types.Integer, primary_key=True),
        Column("code", types.UnicodeText),
        Column("description", types.UnicodeText),
        Column("data_type", types.UnicodeText),
    )    


    # Map those tables to classes, define the additional properties for related people
    meta.mapper(BulkUpload, bulkupload,
        properties={
            "uploaded_user": relationship(model.User)            
        }
    )
    meta.mapper(StandingData, standingdata)
    
    # Stick these classes into the CKAN.model, for ease of access later
    model.BulkUpload = BulkUpload
    model.StandingData = StandingData
    
    return bulkupload

def db_setup():
    """Create tables in the database"""
    # These tables will already be defined in memory if the metadata plugin is enabled.
    #  IConfigurer will make a call to define_tables()
    
    
    bulkupload = meta.metadata.tables.get("bulk_upload", None)
    standingdata = meta.metadata.tables.get("standing_data", None)
    #print "bulkupload: ",bulkupload
    
    if bulkupload == None:
        # The tables have not been defined. Its likely that the plugin is not enabled in the CKAN .ini file
        log.debug("Could not create additional tables. Please make sure that you've added the metadata plugin to your CKAN config .ini file.")
    else:    
        log.debug('Additional Metadata tables defined in memory')
        
        # Alright. Create the tables.
        from ckanext.ngds.base.commands.ngds_tables import create_tables
        create_tables([bulkupload,standingdata], log)