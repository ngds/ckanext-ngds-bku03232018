import logging
import datetime

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import types

from ckanext.ngds.common import model

log = logging.getLogger(__name__)

class SysadminConfigDomainObject(model.domain_object.DomainObject):

    @classmethod
    def get(cls, **kwargs):
        query = model.meta.Session.query(cls).autoflush(False)
        return query.filter_by(**kwargs)

class SysadminConfig(SysadminConfigDomainObject):
    pass

sysadmin_config_table = Table('sysadmin_configurations', model.meta.metadata,
    Column('id', types.UnicodeText, primary_key=True,
           default=model.types.make_uuid),
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

def init_db(data):
    if not sysadmin_config_table.exists():
        sysadmin_config_table.create()

        model.meta.mapper(
            SysadminConfig,
            sysadmin_config_table
        )

        out = SysadminConfig()

        items = ['ngds_publish', 'ngds_harvest', 'ngds_edit_metadata',
                 'ckan_site_title', 'ckan_main_css', 'ckan_site_description',
                 'ckan_site_logo', 'ckan_site_about', 'ckan_site_intro_text',
                 'ckan_homepage_style']

        for item in items:
            setattr(out, item, data.get(item))

        out.save()
        session = model.Session
        session.add(out)
        session.commit()

        log.debug('Sysadmin configuration table created')
    else:
        log.debug('Sysadmin configuration table already exists')

