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

from ckan.model.domain_object import DomainObject
from ckan.model import meta

from sqlalchemy import types, Column, Table, ForeignKey
from sqlalchemy.orm import relationship

class AdditionalPackageMetadata(DomainObject):
    """Adjustments to Package metadata"""
    package_id = None
    author = None
    maintainer = None
    pub_date = None
    
    def __init__(self, package_id=None, **kwargs):
        self.package_id = package_id # Relate this content to a Package
        self.author = kwargs.get('author', None) # author should be a ResponsibleParty
        self.maintainer = kwargs.get('maintainer', None) # maintainer should be a ResponsibleParty
        self.pub_date = kwargs.get('pub_date', None)

class AdditionalResourceMetadata(DomainObject):
    """Adjustments to Resource Metadata"""
    
    resource_id = None
    distributor = None
    
    def __init__(self, resource_id=None, **kwargs):
        self.resource_id = resource_id
        self.distributor = kwargs.get('distributor', None)
              
class ResponsibleParty(DomainObject):
    """
    A ResponsibleParty represents an individual or organization responsible
    for authorship, maintenance, or distribution of a resource
    """
    
    name = None
    email = None
    organization = None
    phone = None
    street = None
    state = None
    city = None
    zip = None
    
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
            "author": relationship(ResponsibleParty, primaryjoin="package_additional_metadata.author_id==responsible_party.id"),
            "maintainer": relationship(ResponsibleParty, primaryjoin="package_additional_metadata.maintainer_id==responsible_party.id")
        }
    )
    
    meta.mapper(
        AdditionalResourceMetadata, 
        resource_meta,
        properties={
            "distributor": relationship(ResponsibleParty)            
        }
    )
    
    return party, resource_meta, package_meta
