''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

from ckanext.ngds.base.model.ngds_db_object import NgdsDataObject
from ckanext.ngds.metadata.model.additional_metadata import ResponsibleParty

from ckan import model
from ckan.model import meta, Package

from sqlalchemy import types, Column, Table, ForeignKey
from sqlalchemy.orm import relationship, validates

import logging
log = logging.getLogger(__name__)

from datetime import datetime

from urlparse import urlparse, urlunparse
from urllib import urlencode
from urllib2 import urlopen

from lxml import etree
from owslib.iso import MD_Metadata
from owslib.csw import CatalogueServiceWeb
from shapely.geometry import box
import json

class HarvestNode(NgdsDataObject):
    """Stores information about harvest endpoints"""
    csw = None
    
    def __init__(self, url, **kwargs):
        # A URL must be given
        p = urlparse(url)
        self.url = urlunparse((p.scheme, p.netloc, p.path, "", "", "")) # Strip URL to just domain + path
        self.frequency = kwargs.get('frequency', 'manual') # frequency should be one of manual|daily|weekly|monthly
        self.title = kwargs.get('title', 'No Title Was Given') # A title for bookkeeping
        self.node_admin_id = kwargs.get('node_admin_id', None) # Foreign Key to a responsible_party who maintains the remote node
        #self.csw = CatalogueServiceWeb(self.url) # owslib CSW class provides mechanisms for making CSW requests
    
    def setup_csw(self):
        self.csw = CatalogueServiceWeb(self.url)
        
    def do_harvest(self):
        """Perform a harvest from another CSW server"""
        if self.csw == None:
            self.setup_csw()                      
        self.get_records() # Do the first GetRecords request
        ids = self.csw.records.keys() # Start an array to house all of the ids
        print "next: %s, total: %s" % (self.csw.results["nextrecord"], self.csw.results["matches"])
        
        while self.csw.results["nextrecord"] < self.csw.results["matches"] and self.csw.results["nextrecord"] != 0: # Once next_record > number_matched, we've gotten everything
            self.get_records(self.csw.results["nextrecord"], self.csw.results["returned"]) # Get another set, starting from next_record from previous response
            ids += self.csw.records.keys() # Add new ids to the array
            print "next: %s, total: %s" % (self.csw.results["nextrecord"], self.csw.results["matches"])
        
        self.parse_records(ids) # Gather the records themselves
                   
    def parse_records(self, ids):
        """Perform as many GetRecordById requests as needed"""
        print "Gathered %s IDs" % str(len(ids))
        for record_id in ids:
            self.get_record_by_id(record_id)
            rec = HarvestedRecord.from_md_metadata(self.csw.records[record_id], self)
    
    def get_record_by_id(self, record_id):
        """Get a single record, by ID"""
        params = {
            "id": [ record_id ],
            "outputschema": "http://www.isotc211.org/2005/gmd"    
        }
        self.csw.getrecordbyid(**params) # Puts response in self.csw.records        
    
    def get_records(self, start_position=1, max_records=1000):
        """Perform a GetRecords request"""
        params = {
            "typenames": "gmd:MD_Metadata",
            "outputschema": "http://www.isotc211.org/2005/gmd",
            "startposition": start_position,
            "maxrecords": max_records,
            "esn": "brief"          
        }
        self.csw.getrecords(**params) # Puts results in self.csw.records        
        
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
            
    @classmethod
    def from_md_metadata(cls, md, harvest_node):
        """Given a MD_Metadata record parsed by owslib, create a Package and HarvestedRecord"""
        def generate_geojson():
            # If there's a bounding box this will work, otherwise it won't
            bbox = md.identification.extent.boundingBox
            shape = { 
                "type": "Polygon", 
                "coordinates": [[
                    [float(bbox.minx), float(bbox.miny)], 
                    [float(bbox.maxx), float(bbox.miny)], 
                    [float(bbox.maxx), float(bbox.maxy)], 
                    [float(bbox.minx), float(bbox.maxy)]
                ]] 
             }
            return json.dumps(shape)
        
        
        additional_parameters = {
            "id": md.identifier, # will CKAN let us state the ID for a package? No.
            "metadata_modified": md.datestamp, # this is a string in owslib
            "notes": md.identification.abstract,
            "title": md.identification.title,
            "tags": [
                { "name": "my-tag", "vocabulary_id": "test" }         
            ], # tough logic that will need to amalgamate keywords. Will I loose thesaurus info? CKAN's tag logic is confusing, too
            "extras": [
                { "key": "dataset_uri", "value": md.dataseturi }, # this can probably be an array?
                { "key": "dataset_category", "value": md.hierarchy },
                { "key": "pans", "value": md.identification.date[0].date }, # this is a string in owslib, should find the obj in the date array where type="publication"
                { "key": "creators", "value": [] }, # complex procedure involves adding ResponsibleParties  
                { "key": "quality", "value": ""}, # md.dataquality }, # md.dataquality is DQ_DataQuality is retarded.
                { "key": "status", "value": md.identification.status },
                { "key": "dataset_lang", "value": next((val for idx, val in enumerate(md.identification.resourcelanguage)), "") }, # this is an array in owslib. Tricky logic to essentially return either the first entry in the array or an empty string
                { "key": "spatial_word", "value": "" }, # tough logic to find any location keywords
                { "key": "spatial", "value": generate_geojson() }, 
                { "key": "usage", "value": next((val for idx, val in enumerate(md.identification.useconstraints)), "") } # array in owslib         
            ]
        }
        
        package_parameters = { # These are the fields required by CKAN
            "maintainer": "",
            "title": "",
            "name": md.identifier, # this is the package's URL
            "author_email": "",
            "notes": "",
            "author": "",
            "maintainer_email": "",
            "license_id": "notspecified"
        }
        
        package_parameters.update(additional_parameters)
        
        from ckan.logic import get_action
        pkg = get_action('package_create')(None, package_parameters)
        print "Made a package?"        
        
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
        Column("frequency", types.UnicodeText),
        Column("title", types.UnicodeText),
        Column("node_admin_id", types.Integer, ForeignKey("responsible_party.id"))                
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
    meta.mapper(HarvestNode, node_table,
        properties={
            "node_admin": relationship(ResponsibleParty)            
        }
    )
    
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

        
        

        
        
