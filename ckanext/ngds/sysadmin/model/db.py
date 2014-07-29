import logging
import datetime

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import types

log = logging.getLogger(__name__)

SysadminConfig = None
sysadmin_config_table = None

def init(model):
    global SysadminConfig
    class SysadminConfig(model.DomainObject):

        @classmethod
        def get(cls, **kwargs):
            query = model.meta.Session.query(cls).autoflush(False)
            return query.filter_by(**kwargs)

    global sysadmin_config_table
    sysadmin_config_table = Table('sysadmin_configurations', model.meta.metadata,
        Column('id', types.UnicodeText, primary_key=True,
               default=model.types.make_uuid),
        Column('last_edited', types.DateTime, default=datetime.datetime.utcnow),
        Column('active_config', types.Boolean, default=True),
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

    if sysadmin_config_table.exists():
        log.debug('Sysadmin configuration table already exists')
    else:
        sysadmin_config_table.create()
        log.debug('Sysadmin configuration table created')

    model.meta.mapper(
        SysadminConfig,
        sysadmin_config_table
    )

def init_table_populate(model, data):
    if sysadmin_config_table is None:
        init(model)
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

def init_config_show(model):
    if sysadmin_config_table is None:
        init(model)
    out = SysadminConfig.get(active_config=True)
    return [{'last_edited': o.last_edited,
             'active_config': o.active_config,
             'ngds_publish': o.ngds_publish,
             'ngds_harvest': o.ngds_harvest,
             'ngds_edit_metadata': o.ngds_edit_metadata,
             'ckan_site_title': o.ckan_site_title,
             'ckan_main_css': o.ckan_main_css,
             'ckan_site_description': o.ckan_site_description,
             'ckan_site_logo': o.ckan_site_logo,
             'ckan_site_about': o.ckan_site_about,
             'ckan_site_intro_text': o.ckan_site_intro_text,
             'ckan_homepage_style': o.ckan_homepage_style,
            } for o in out]
