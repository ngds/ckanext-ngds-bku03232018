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


from ckan.model import meta

from sqlalchemy import types, Column, Table, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql.expression import or_ 

from sqlalchemy import types, Column, Table
from sqlalchemy.orm import validates

from pylons import config

import csv
import logging
log = logging.getLogger(__name__)

from ckanext.ngds.base.model.ngds_db_object import NgdsDataObject
        
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
        self.country = kwargs.get('country', None)
        
    @classmethod
    def search(cls, querystr, sqlalchemy_query=None):
        '''Search name, fullname, email and openid. '''
        if sqlalchemy_query is None:
            query = meta.Session.query(cls)
        else:
            query = sqlalchemy_query
        
        qstr = '%' + querystr + '%'
        query = query.filter(or_(
            cls.name.ilike(qstr),
            cls.email.ilike(qstr)
            ))
        print query
        return query
    # Vivek - Put this in here temporarily to explore if this works.

    @classmethod
    def get(cls, reference):
        '''Returns a group object referenced by its id or name.'''
        query = meta.Session.query(cls).filter(cls.id == reference)
        member = query.first()
        if member is None:
            member = cls.by_name(reference)
        return member

    def find(cls,email):
        '''Returns responsible party details with matching name and/ email. If the email is None then get the detail matching only name '''
        
        if email is None:
            raise Exception("Email can't be empty for finding the responsible party")

        query = meta.Session.query(cls)
        
        query = query.filter(cls.email.lower() == email.lower())

        return query


class Language(NgdsDataObject):
    """
    A ResponsibleParty represents an individual or organization responsible
    for authorship, maintenance, or distribution of a resource
    """
    
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.code = kwargs.get('code', None)
        self.standard = kwargs.get('standard', None)
        
    @classmethod
    def search(cls, querystr, sqlalchemy_query=None):
        '''Search name, fullname, email and openid. '''
        if sqlalchemy_query is None:
            query = meta.Session.query(cls)
        else:
            query = sqlalchemy_query
        
        qstr = '%' + querystr + '%'
        query = query.filter(or_(
            cls.name.ilike(qstr),
            cls.code.ilike(qstr)
            ))
        print query
        return query
    # Vivek - Put this in here temporarily to explore if this works.

    @classmethod
    def get(cls, reference):
        '''Returns a group object referenced by its id or name.'''
        query = meta.Session.query(cls).filter(cls.id == reference)
        member = query.first()
        if member is None:
            member = cls.by_name(reference)
        return member


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
        Column("zip", types.UnicodeText),
        Column("country", types.UnicodeText)
    )
    
    languages = Table(
        "languages",
        meta.metadata,
        Column("id", types.Integer, primary_key=True),
        Column("name", types.UnicodeText),
        Column("code", types.UnicodeText),
        Column("standard", types.UnicodeText)
    )

    # Map those tables to classes, define the additional properties for related people
    meta.mapper(ResponsibleParty, party)
    meta.mapper(Language, languages)
    
    # Stick these classes into the CKAN.model, for ease of access later
    model.ResponsibleParty = ResponsibleParty
    model.Language = Language
    
    return party, languages

def db_setup():
    """Create tables in the database"""
    # These tables will already be defined in memory if the metadata plugin is enabled.
    #  IConfigurer will make a call to define_tables()
    
    
    party = meta.metadata.tables.get("responsible_party", None)
    languages = meta.metadata.tables.get("languages", None)
    
    if party == None:
        # The tables have not been defined. Its likely that the plugin is not enabled in the CKAN .ini file
        log.debug("Could not create additional tables. Please make sure that you've added the metadata plugin to your CKAN config .ini file.")
    else:    
        log.debug('Additional Metadata tables defined in memory')
        
        # Alright. Create the tables.
        from ckanext.ngds.base.commands.ngds_tables import create_tables
        create_tables([party, languages], log)
        populate_languages()

def populate_languages():
    resources_dir = config.get('ngds.resources_dir')
    if resources_dir:
       
       if(resources_dir[-1]=='/'):
            resources_dir = resources_dir[0:len(resources_dir)-1]
       
       lang_csv_file = open(resources_dir+'/db/iso6392_languages.csv')
       reader = csv.reader(lang_csv_file,delimiter=",")
       languages_list = []
       session = meta.Session

       for row in reader:
            name = row[0]
            code = row[1]
            standard = row[2]
            lang_dict = { "name":name, "code":code,"standard":standard }
            language = model.Language(**lang_dict)
            languages_list.append(language)

       session.add_all(languages_list)
       session.commit()


    else:
        log.debug("You need to specify the absolute path to ckanext-ngds/ckanext/ngds/base/resources for db init")
