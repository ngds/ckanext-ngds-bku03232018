from ckanext.ngds.base.model.ngds_db_object import NgdsDataObject

from ckan import model
from ckan.model import meta, Package

from sqlalchemy import types, Column, Table, ForeignKey
from sqlalchemy.orm import relationship, validates

import logging
log = logging.getLogger(__name__)

from datetime import datetime

class HarvestNode(NgdsDataObject):
    """Stores information about harvest endpoints"""
    def __init__(self, url, **kwargs):
        self.url = url # A URL must be given
        self.frequency = kwargs.get('frequency', 'manual') # frequency should be one of manual|daily|weekly|monthly

class HarvestedRecord(NgdsDataObject):
    """Store relationship between a harvest node and a CKAN package"""
    def __init__(self, package_id, harvest_node_id, harvested_xml):
        self.package_id = package_id
        self.harvest_node_id = harvest_node_id
        self.harvested_xml = harvested_xml
    
    @validates('package_id')
    def validate_package_id(self, key, package_id):
        """Check that the package_id given is valid"""
        pkg = self.Session.query(Package).filter(getattr(Package, "id", None)==package_id).first() # Check if a package with that ID already exists
        if pkg:
            return package_id
        else:
            assert False
'''
This stuff is started, but not sure if I actually want to do it this way

class HarvestLog(NgdsDataObject):
    """Persist harvesting history"""
    def __init__(self, harvest_node_id, **kwargs):
        self.harvest_node_id = harvest_node_id
        self.harvest_date = kwargs.get('harvest_date', datetime.now().date())
        self.records_harvested = kwargs.get('records_harvested', 0)
        self.success = kwargs.get('success', False)
        
class HarvestLogEntry(NgdsDataObject):
    def __init__(self, harvest_log_id, message):
        self.harvest_log_id = harvest_log_id
        self.message = message
'''
        
def define_tables():
    """Create in-memory representation of the harvest tables"""
    # Define the tables
    node_table = Table(
        "harvest_node",
        meta.metadata,
        Column("id", types.Integer, primary_key=True),
        Column("url", types.UnicodeText),
        Column("frequency", types.UnicodeText)                   
    )
    
    harvest_record_table = Table(
        "harvested_record",
        meta.metadata,
        Column("id", types.Integer, primary_key=True),
        Column("package_id", types.UnicodeText, ForeignKey("package.id")),
        Column("harvest_node_id", types.Integer, ForeignKey("harvest_node.id")),
        Column("harvested_xml", types.UnicodeText)                             
    )
    
    # Map classes to tables
    meta.mapper(HarvestNode, node_table)
    
    meta.mapper(
        HarvestedRecord,
        harvest_record_table, 
        properties={
            "package": relationship(Package),
            "harvest_node": relationship(HarvestNode)
        }
    )
    
    # Add classes to memory
    model.HarvestNode = HarvestNode
    model.HarvestedRecord = HarvestedRecord
    
def db_setup():
    """Create database tables"""
    node_table = meta.metadata.tables.get("harvest_node", None)
    harvest_record_table = meta.metadata.tables.get("harvested_record", None)
    
    if node_table == None or harvest_record_table == None:
        log.debug("Could not create additional tables. Please make sure that you've added the ngdsharvest plugin to your CKAN config .ini file.")
    else:
        log.debug("NGDS Harvesting tables defined in memory")
        from ckanext.ngds.base.commands.ngds_tables import create_tables
        create_tables([node_table, harvest_record_table], log)

        
        

        
        