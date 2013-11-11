from sqlalchemy import Column, Table, String, Text, Integer, types, ForeignKey
from sqlalchemy.orm import relationship

from ckan import model
from ckan.model import meta, Package

from shapely.geometry import asShape
import json

import logging
log = logging.getLogger(__name__)

class CswRecord(object):
    """
    Class representing CSW Records that are stored in the database and served via CSW
    """
    def __init__(self, package_id=None, **kwargs):
        self.package_id = package_id
        self.identifier = kwargs.get("identifier", None)
        self.typename = kwargs.get("typename", None)
        self.schema = kwargs.get("schema", None)
        self.mdsource = kwargs.get("mdsource", None)
        self.insert_date = kwargs.get("insert_date", None)
        self.xml = kwargs.get("xml", None)
        self.anytext = kwargs.get("anytext", None)
        self.language = kwargs.get("language", None)
        self.type = kwargs.get("type", None)
        self.title = kwargs.get("title", None)
        self.title_alternate = kwargs.get("title_alternate", None)
        self.abstract = kwargs.get("abstract", None)
        self.keywords = kwargs.get("keywords", None)
        self.keywordstype = kwargs.get("keywordstype", None)
        self.parentidentifier = kwargs.get("parentidentifier", None)
        self.relation = kwargs.get("relation", None)
        self.time_begin = kwargs.get("time_begin", None)
        self.time_end = kwargs.get("time_end", None)
        self.topicategory = kwargs.get("topicategory", None)
        self.resourcelanguage = kwargs.get("resourcelanguage", None)
        self.creator = kwargs.get("creator", None)
        self.publisher = kwargs.get("publisher", None)
        self.contributor = kwargs.get("contributor", None)
        self.organization = kwargs.get("organization", None)
        self.securityconstraints = kwargs.get("securityconstraints", None)
        self.accessconstraints = kwargs.get("accessconstraints", None)
        self.otherconstraints = kwargs.get("otherconstraints", None)
        self.date = kwargs.get("date", None)
        self.date_revision = kwargs.get("date_revision", None)
        self.date_creation = kwargs.get("date_creation", None)
        self.date_publication = kwargs.get("date_publication", None)
        self.date_modified = kwargs.get("date_modified", None)
        self.format = kwargs.get("format", None)
        self.source = kwargs.get("source", None)
        self.crs = kwargs.get("crs", None)
        self.geodescode = kwargs.get("geodescode", None)
        self.distancevalue = kwargs.get("distancevalue", None)
        self.distanceuom = kwargs.get("distanceuom", None)
        self.wkt_geometry = kwargs.get("wkt_geometry", None)
        self.servicetype = kwargs.get("servicetype", None)
        self.servicetypeversion = kwargs.get("servicetypeversion", None)
        self.operation = kwargs.get("operation", None)
        self.couplingtype = kwargs.get("couplingtype", None)
        self.operateson = kwargs.get("operateson", None)
        self.operatesonidentifier = kwargs.get("operatesonidentifier", None)
        self.operatesoname = kwargs.get("operatesoname", None)
        self.degree = kwargs.get("degree", None)
        self.classification = kwargs.get("classification", None)
        self.conditionapplyingtoaccessanduse = kwargs.get("conditionapplyingtoaccessanduse", None)
        self.lineage = kwargs.get("lineage", None)
        self.responsiblepartyrole = kwargs.get("responsiblepartyrole", None)
        self.specificationtitle = kwargs.get("specificationtitle", None)
        self.specificationdate = kwargs.get("specificationdate", None)
        self.specificationdatetype = kwargs.get("specificationdatetype", None)
        self.links = kwargs.get("links", None)                
    
    @classmethod
    def format_links(cls, resources):
        '''Format links for pycsw usage: "name,description,protocol,url[^,,,[^,,,]]"'''
        links = []
        for resource in resources:
            link = "%s," % resource["name"]
            link += "%s," % resource["description"]
            link += "%s," % resource["protocol"]
            link += "%s" % resource["url"]
            links.append(link)
            
        return "^".join(links)
    
    @classmethod
    def format_keywords(cls, iso_package):
        keywords = [ keyword.name for keyword in iso_package.dataset_info["keywords"] ]
        if iso_package.dataset_info["extent_keyword"]:
            keywords.append(iso_package.dataset_info["extent_keyword"])
        return ",".join(keywords)
    
    @classmethod
    def from_iso_package(cls, iso_package):
        """Create an instance of CswRecord from an ckanext.ngds.metadata.model.iso_package:IsoPackage"""
        creation_args = {
            "package_id": iso_package.ckan_package.id,
            "identifier": iso_package.metadata_info["id"],
            "typename": "gmd:MD_Metadata",
            "schema": "http://www.isotc211.org/2005/gmd",
            "mdsource": "local",
            "insert_date": iso_package.metadata_info["updated"].replace(microsecond=0).isoformat(),
            "xml": iso_package.to_iso_xml(),
            "anytext": "",
            "language": iso_package.metadata_info["language"],
            "type": iso_package.dataset_info["category"],
            "title": iso_package.dataset_info["title"],
            "abstract": iso_package.dataset_info["abstract"],
            "keywords": cls.format_keywords(iso_package),
            "keywordstype": "theme",
            "parentIdentifier": None,
            "relation": "",
            "time_begin": None,
            "time_end": None,
            "topicategory": iso_package.dataset_info["topic"],
            "resourcelanguage": iso_package.dataset_info["language"],
            "creator": "creator",
            "publisher": "publisher",
            "contributor": "contributor",
            "organization": None,
            "securityconstraints": None,
            "accessconstraints": iso_package.dataset_info["usage"],
            "otherconstraints": None,
            "date": iso_package.metadata_info["updated"].replace(microsecond=0).isoformat(),
            "date_revision": None,
            "date_creation": None,
            "date_publication": iso_package.dataset_info["publication_date"].replace(microsecond=0).isoformat(),
            "date_modified": None,
            "format": None,
            "source": None,
            "crs": None,
            "geodescode": None,
            "denominator": None,
            "distancevalue": None,
            "distanceuom": None,
            "wkt_geometry": asShape(json.loads(iso_package.dataset_info["extent"])).wkt,
            "servicetype": None,
            "servicetypeversion": None,
            "operation": None,
            "couplingtype": None,
            "operateson": None,
            "operatesonidentifier": None,
            "degree": None,
            "conditionapplyingtoaccessanduse": None,
            "lineage": None,
            "responsiblepartyrole": "distributor", # huh?
            "specificationtitle": None,
            "specificationdate": None,
            "spcificationdatetype": None,
            "links": cls.format_links(iso_package.resources)
        }
        
        record = cls(**creation_args)
        return record
    
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
        Column('title', types.UnicodeText, index=True),
        Column('title_alternate', types.UnicodeText, index=True),
        Column('abstract', types.UnicodeText, index=True),
        Column('keywords', types.UnicodeText, index=True),
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
        
        