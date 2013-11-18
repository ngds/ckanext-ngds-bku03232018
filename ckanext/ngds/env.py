''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

"""
Sometimes we need access to CKAN objects that we can't get at through
    ckan.plugins.toolkit. If we import those things here and need to adjust
    in the future, we can do that adjustment in one place.

This also allows us to "spoof" CKAN objects we need, without relying directly on CKAN, e.g. Session
"""

# If you have to use ckan.model...
from ckan import model as ckan_model
from ckan import logic as ckan_logic
from ckan import lib as ckan_lib
from pylons import config as ckan_config
from sqlalchemy import create_engine
import ckan.lib.helpers as h
from sqlalchemy.orm import sessionmaker
import ckan.lib.base as base

_ = base._

# Create a CKAN database session without relying on CKAN
def _setup(dburl):
    """Define a SQLAlchemy Session from ckan_config"""
    db_str = ckan_config.get(dburl)
    return sessionmaker(bind=create_engine(db_str, echo=False))


Session = _setup("sqlalchemy.url")

DataStoreSession = _setup("ckan.datastore.write_url")
