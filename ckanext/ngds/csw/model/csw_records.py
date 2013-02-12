from sqlalchemy import Column, Table, String, Text, Integer, types, ForeignKey
from sqlalchemy.orm import relationship

from ckan import model
from ckan.model import meta, Package

from ckanext.ngds.base.model.ngds_db_object import NgdsDataObject

import logging
log = logging.getLogger(__name__)

class CswRecord(NgdsDataObject):
    """
    Class representing CSW Records that are stored in the database and served via CSW
    
    INCOMPLETE
    """
    def __init__(self, package_id=None, **kwargs):
        self.package_id = package_id

def define_tables():
    """
    Create in-memory representation of the tables, configure mappings to 
    python classes, and return the tables
    
    Table generation code is lifted from pycsw
    """
    csw_record = Table(
        "csw_record", meta.metadata,
        
        Column('package_id', types.UnicodeText, ForeignKey("package.id")), # Implicit Foreign Key to the package
        
        # core; nothing happens without these
        Column('identifier', String(256), primary_key=True),
        Column('typename', String(32),
               default='csw:Record', nullable=False, index=True),
        Column('schema', String(256),
               default='http://www.opengis.net/cat/csw/2.0.2', nullable=False,
               index=True),
        Column('mdsource', String(256), default='local', nullable=False,
               index=True),
        Column('insert_date', String(20), nullable=False, index=True),
        Column('xml', Text, nullable=False),
        Column('anytext', Text, nullable=False),
        Column('language', String(32), index=True),

        # identification
        Column('type', String(128), index=True),
        Column('title', String(2048), index=True),
        Column('title_alternate', String(2048), index=True),
        Column('abstract', String(2048), index=True),
        Column('keywords', String(2048), index=True),
        Column('keywordstype', String(256), index=True),
        Column('parentidentifier', String(32), index=True),
        Column('relation', String(256), index=True),
        Column('time_begin', String(20), index=True),
        Column('time_end', String(20), index=True),
        Column('topicategory', String(32), index=True),
        Column('resourcelanguage', String(32), index=True),

        # attribution
        Column('creator', String(256), index=True),
        Column('publisher', String(256), index=True),
        Column('contributor', String(256), index=True),
        Column('organization', String(256), index=True),

        # security
        Column('securityconstraints', String(256), index=True),
        Column('accessconstraints', String(256), index=True),
        Column('otherconstraints', String(256), index=True),

        # date
        Column('date', String(20), index=True),
        Column('date_revision', String(20), index=True),
        Column('date_creation', String(20), index=True),
        Column('date_publication', String(20), index=True),
        Column('date_modified', String(20), index=True),

        Column('format', String(128), index=True),
        Column('source', String(1024), index=True),

        # geospatial
        Column('crs', String(256), index=True),
        Column('geodescode', String(256), index=True),
        Column('denominator', Integer, index=True),
        Column('distancevalue', Integer, index=True),
        Column('distanceuom', String(8), index=True),
        Column('wkt_geometry', Text),

        # service
        Column('servicetype', String(32), index=True),
        Column('servicetypeversion', String(32), index=True),
        Column('operation', String(256), index=True),
        Column('couplingtype', String(8), index=True),
        Column('operateson', String(32), index=True),
        Column('operatesonidentifier', String(32), index=True),
        Column('operatesoname', String(32), index=True),

        # additional
        Column('degree', String(8), index=True),
        Column('classification', String(32), index=True),
        Column('conditionapplyingtoaccessanduse', String(256), index=True),
        Column('lineage', String(32), index=True),
        Column('responsiblepartyrole', String(32), index=True),
        Column('specificationtitle', String(32), index=True),
        Column('specificationdate', String(20), index=True),
        Column('specificationdatetype', String(20), index=True),

        # distribution
        # links: format "name,description,protocol,url[^,,,[^,,,]]"
        Column('links', Text, index=True),
    )
    
    # Map the table to the class...
    meta.mapper(
        CswRecord, 
        csw_record,
        properties={
            "package": relationship(Package)
        }
    )
    
    # put the CswRecord class intp CKAN model for later reference
    model.CswRecord = CswRecord
    
    return csw_record
    
def db_setup():
    """Create tables in the database"""
    # These tables will already be defined in memory if the csw plugin is enabled.
    #  IConfigurer will make a call to define_tables()
    csw_record = meta.metadata.tables.get("csw_record", None)
    
    if csw_record == None:
        # The tables have not been defined. Its likely that the plugin is not enabled in the CKAN .ini file
        log.debug("Could not create CSW tables. Please make sure that you've added the csw plugin to your CKAN config .ini file.")
    else:    
        log.debug('CSW tables defined in memory')
        
        # Alright. Create the tables.
        from ckanext.ngds.base.commands.ngds_tables import create_tables
        create_tables([csw_record], log)
        
        