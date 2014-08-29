import logging
import datetime

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import types
from sqlalchemy.orm import class_mapper

log = logging.getLogger(__name__)

SysadminConfig = None
ngds_system_info = None

def init(model):
    """
    Method for building the 'ngds_system_info' table in the database, creating
    an object for the ORM andcreating the ORM.

    @model: base CKAN model object
    @return: nothing, instead we rely on global objects *sigh*
    """

    # Object with methods for accessing the database table we create.
    global SysadminConfig
    class SysadminConfig(model.DomainObject):
        # Return the first row that matches the query.  We only ever want one
        # row in this table, so this method works.
        @classmethod
        def get(cls, **kwargs):
            query = model.meta.Session.query(cls).autoflush(False)
            return query.filter_by(**kwargs).first()

    # PostgreSQL table schema per sqlalchemy syntax
    global ngds_system_info
    ngds_system_info = Table('ngds_system_info', model.meta.metadata,
        Column('id', types.UnicodeText, primary_key=True,
               default=model.types.make_uuid),
        Column('last_edited', types.DateTime, default=datetime.datetime.utcnow),
        Column('active_config', types.Boolean, default=True),
        Column('ngds.publish', types.UnicodeText, default=u''),
        Column('ngds.harvest', types.UnicodeText, default=u''),
        Column('ngds.edit_metadata', types.UnicodeText, default=u''),
        Column('ngds.featured_data', types.UnicodeText, default=u'')
    )

    # If/Else to create database table
    if ngds_system_info.exists():
        log.debug('Sysadmin configuration table already exists')
    else:
        ngds_system_info.create()
        log.debug('Sysadmin configuration table created')

    # Bind ORM
    model.meta.mapper(
        SysadminConfig,
        ngds_system_info
    )

def init_table_populate(model, data):
    """
    Populates the database table with default configurations if we're building
    this table for the first time.  This method should only ever be used when
    the server is booting up.

    @param model: base CKAN model object
    @param data: dictionary of default config parameters
    @return: nothing
    """

    # Check for ORM
    if ngds_system_info is None:
        init(model)

    # Check if data exists in the database table
    if SysadminConfig.get(active_config=True):
        pass
    else:
        # If it doesn't, populate database table with default *.ini values
        out = SysadminConfig()
        items = ['ngds.publish', 'ngds.harvest', 'ngds.edit_metadata']
        for item in items:
            setattr(out, item, data.get(item))
        out.save()
        session = model.Session
        session.add(out)
        session.commit()

def init_config_show(model):
    """
    Reads data from the database table and parses it into a dictionary that
    we'll use to update the pylons global config object.  This method should
    only every be used whe the server is booting up.

    @param model: base CKAN model object
    @return: dictionary of data read from database table
    """
    db_config = {}

    # Check for ORM
    if ngds_system_info is None:
        init(model)

    # Read data from database table
    table = SysadminConfig.get(active_config=True)
    mapped_table = class_mapper(table.__class__).mapped_table

    # Parse data into a dictionary
    for key in mapped_table.c.keys():
        db_config[key] = getattr(table, key)

    return db_config