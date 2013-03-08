"""
We need to persist additional metadata in order to build NGDS-compliant
ISO19139 documents.

ckan.model.package:Package defines some things we need:
* title: The title of the package
* notes: A description of, or abstract for the package
* author: The name of the party responsible for creating the package
* author_email: The email address of the author
* maintainer: The name of the party responsible for maintaining the package
* maintainer_email: The email address of the maintainer

ckan.model.resource:Resource represents a "link" to a file or service:
* url: Where the link points to
* resource_type: Indicates file, file.upload or api. Choices may need to expand (WFS, WMS, CSW)
* name: name of the link
* notes: description of the link

ckanext.spatial.model.package_extent:PackageExtent contains:
* spatial extent: The bounding area the package represents.

We need some additional information:
* More robust contact information (address, phone, organization)
* Distinction of author, maintainer and distributor roles
* Publication date: When was it published?
* Tags from a vocabulary: maybe...
* Distributor of a link
* Layer within a link, where applicable
"""

from ckan import model
from ckan.model.domain_object import DomainObject
from ckan.model import meta, Package, Resource

from sqlalchemy import types, Column, Table, ForeignKey
from sqlalchemy.orm import relationship, validates

from datetime import datetime

import logging
log = logging.getLogger(__name__)

from ckanext.ngds.base.model.ngds_db_object import NgdsDataObject
        
class AdditionalPackageMetadata(NgdsDataObject):
    """Adjustments to Package metadata"""
    def __init__(self, package_id=None, **kwargs):
        self.package_id = package_id # Relate this content to a Package
        self.author_id = kwargs.get('author_id', None) # author should be a ResponsibleParty
        self.maintainer_id = kwargs.get('maintainer_id', None) # maintainer should be a ResponsibleParty
        self.pub_date = kwargs.get('pub_date', None)

    @classmethod
    def by_package(cls, package_id):
        """Look up the AdditionalPackageMetadata for a particular package by its ID"""
        return cls.Session.query(cls).filter(cls.package_id==package_id)
    
    @validates('pub_date')
    def validate_pub_date(self, key, pub_date):
        """Check that date was given in a valid format"""
        date_format = "%Y-%m-%d" # expect dates in format YYYY-MM-DD
        try:
            datetime.strptime(pub_date, date_format) # try to convert the string to a Date object
            return pub_date
        except ValueError, e:
            raise e
        
    @validates('package_id')
    def validate_package_id(self, key, package_id):
        """Check that the package_id given is valid"""
        pkg = self.Session.query(Package).filter(Package.id==package_id).first() # Check if a package with that ID already exists
        used = self.Session.query(AdditionalPackageMetadata).filter(AdditionalPackageMetadata.package_id==package_id).first() # Check if this package_id is already in use
        if pkg and not used:
            return package_id
        else:
            assert False
            
class AdditionalResourceMetadata(NgdsDataObject):
    """Adjustments to Resource Metadata"""
    def __init__(self, resource_id=None, **kwargs):
        self.resource_id = resource_id
        self.distributor_id = kwargs.get('distributor_id', None)
        
    @classmethod
    def by_resource(cls, resource_id):
        """Look up the AdditionalResourceMetadata for a particular resource by its ID"""
        return cls.Session.query(cls).filter(cls.resource_id==resource_id)
    
    @validates('resource_id')
    def validate_resource_id(self, key, resource_id):
        """Check that the package_id given is valid"""
        pkg = self.Session.query(Resource).filter(Resource.id==resource_id).first() # Check if a resource with that ID already exists
        used = self.Session.query(AdditionalResourceMetadata).filter(AdditionalResourceMetadata.resource_id==resource_id).first() # Check if this resource_id is already in use
        if pkg and not used:
            return resource_id
        else:
            assert False
            
class ResponsibleParty(NgdsDataObject):
    """
    A ResponsibleParty represents an individual or organization responsible
    for authorship, maintenance, or distribution of a resource
    """
    
    def __init__(self, name, email, **kwargs):
        self.name = name
        self.email = email
        self.organization = kwargs.get('organization', None)
        self.phone = kwargs.get('phone', None)
        self.street = kwargs.get('street', None)
        self.state = kwargs.get('state', None)
        self.city = kwargs.get('city', None)
        self.zip = kwargs.get('zip', None)
        
def define_tables():
    """Create the in-memory represenatation of tables, and map those tables to classes defined above"""
    
    # First define the three tables
    party = Table(
        "responsible_party",
        meta.metadata,
        Column("id", types.Integer, primary_key=True),
        Column("name", types.UnicodeText),
        Column("email", types.UnicodeText),
        Column("organization", types.UnicodeText),
        Column("phone", types.UnicodeText),
        Column("street", types.UnicodeText),
        Column("state", types.UnicodeText),
        Column("city", types.UnicodeText),
        Column("zip", types.UnicodeText)
    )
    
    resource_meta = Table(
        "resource_additional_metadata", # table name
        meta.metadata, # sqlalchemy.MetaData()
        Column("resource_id", types.UnicodeText, primary_key=True), # Implicit Foreign Key to the resource
        Column("distributor_id", types.Integer, ForeignKey("responsible_party.id")) # Foreign Key to a ResponsibleParty                                          
    )
    
    package_meta = Table(
        'package_additional_metadata', # table name
        meta.metadata, # Apparently just a call to sqlalchemy.MetaData(), whatever that is
        Column('package_id', types.UnicodeText, primary_key=True), # Implicit Foreign Key to the package
        Column('author_id', types.Integer, ForeignKey("responsible_party.id")), # Foreign Key to a ResponsibleParty
        Column('maintainer_id', types.Integer, ForeignKey("responsible_party.id")), # Foreign Key to a ResponsibleParty
        Column('pub_date', types.Date) # Publication Date
    )
    
    # Map those tables to classes, define the additional properties for related people
    meta.mapper(ResponsibleParty, party)
    
    meta.mapper(
        AdditionalPackageMetadata, 
        package_meta,
        properties={
            "author": relationship(ResponsibleParty, primaryjoin=package_meta.columns.get("author_id")==party.columns.get("id")),#"package_additional_metadata.author_id==responsible_party.id"),
            "maintainer": relationship(ResponsibleParty, primaryjoin=package_meta.columns.get("maintainer_id")==party.columns.get("id"))#"package_additional_metadata.maintainer_id==responsible_party.id")
        }
    )
    
    meta.mapper(
        AdditionalResourceMetadata, 
        resource_meta,
        properties={
            "distributor": relationship(ResponsibleParty)            
        }
    )
    
    # Stick these classes into the CKAN.model, for ease of access later
    model.AdditionalPackageMetadata = AdditionalPackageMetadata
    model.AdditionalResourceMetadata = AdditionalResourceMetadata
    model.ResponsibleParty = ResponsibleParty
    
    return party, resource_meta, package_meta

def db_setup():
    """Create tables in the database"""
    # These tables will already be defined in memory if the metadata plugin is enabled.
    #  IConfigurer will make a call to define_tables()
    
    
    party = meta.metadata.tables.get("responsible_party", None)
    package_meta = meta.metadata.tables.get("package_additional_metadata", None)
    resource_meta = meta.metadata.tables.get("resource_additional_metadata", None)
    
    if party == None or package_meta == None or resource_meta == None:
        # The tables have not been defined. Its likely that the plugin is not enabled in the CKAN .ini file
        log.debug("Could not create additional tables. Please make sure that you've added the metadata plugin to your CKAN config .ini file.")
    else:    
        log.debug('Additional Metadata tables defined in memory')
        
        # Alright. Create the tables.
        from ckanext.ngds.base.commands.ngds_tables import create_tables
        create_tables([party, package_meta, resource_meta], log)
