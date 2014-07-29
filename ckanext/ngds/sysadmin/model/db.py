import logging
import datetime

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import types

from ckanext.ngds.common.model.meta import metadata, mapper, Session
from ckanext.ngds.common.model.types import make_uuid
from ckanext.ngds.common.model.domain_object import DomainObject

log = logging.getLogger(__name__)

class SysadminConfigDomainObject(DomainObject):

    @classmethod
    def get(cls, **kwargs):
        query = Session.query(cls).autoflush(False)
        return query.filte_by(**kwargs)

class SysadminConfig(SysadminConfigDomainObject):
    pass

sysadmin_config_table = Table('sysadmin_configurations', metadata,
    Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
    Column('last_edited', types.DateTime, default=datetime.datetime.utcnow),
    Column('ngds_publish', types.UnicodeText, default=u''),
    Column('ngds_harvest', types.UnicodeText, default=u''),
    Column('ngds_edit_metadata', types.UnicodeText, default=u''),
    Column('ckan_site_title', types.UnicodeText, default=u''),
    Column('ckan_main_css', types.UnicodeText, default=u''),
    Column('ckan_site_description', types.UnicodeText, default=u''),
    Column('ckan_site_logo', types.UnicodeText, default=u''),
    Column('ckan_site_about', types.UnicodeText, default=u''),
    Column('ckan_site_intro_text', types.UnicodeText, default=u''),
    Column('ckan_homepage_style', types.UnicodeText, default=u''),
)

def init_db():
    if not sysadmin_config_table.exists():
        sysadmin_config_table.create()
        log.debug('Sysadmin configuration table created')
    else:
        log.debug('Sysadmin configuration table already exists')

    mapper(
        SysadminConfig,
        sysadmin_config_table
    )