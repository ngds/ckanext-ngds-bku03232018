import logging
import datetime

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import types
from sqlalchemy.orm import class_mapper

log = logging.getLogger(__name__)

SysadminConfig = None
sysadmin_config_table = None

def init(model):
    global SysadminConfig
    class SysadminConfig(model.DomainObject):

        @classmethod
        def get(cls, **kwargs):
            query = model.meta.Session.query(cls).autoflush(False)
            return query.filter_by(**kwargs).first()

    global sysadmin_config_table
    sysadmin_config_table = Table('sysadmin_configurations', model.meta.metadata,
        Column('id', types.UnicodeText, primary_key=True,
               default=model.types.make_uuid),
        Column('last_edited', types.DateTime, default=datetime.datetime.utcnow),
        Column('active_config', types.Boolean, default=True),
        Column('ngds.publish', types.UnicodeText, default=u''),
        Column('ngds.harvest', types.UnicodeText, default=u''),
        Column('ngds.edit_metadata', types.UnicodeText, default=u''),
        Column('ckan.site_title', types.UnicodeText, default=u''),
        Column('ckan.main_css', types.UnicodeText, default=u''),
        Column('ckan.site_description', types.UnicodeText, default=u''),
        Column('ckan.site_logo', types.UnicodeText, default=u''),
        Column('ckan.site_about', types.UnicodeText, default=u''),
        Column('ckan.site_intro_text', types.UnicodeText, default=u''),
        Column('ckan.homepage_style', types.UnicodeText, default=u''),
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

    if SysadminConfig.get(active_config=True):
        pass
    else:
        out = SysadminConfig()
        items = ['ngds.publish', 'ngds.harvest', 'ngds.edit_metadata',
                 'ckan.site_title', 'ckan.main_css', 'ckan.site_description',
                 'ckan.site_logo', 'ckan.site_about', 'ckan.site_intro_text',
                 'ckan.homepage_style']
        for item in items:
            setattr(out, item, data.get(item))
        out.save()
        session = model.Session
        session.add(out)
        session.commit()

def init_config_show(model):
    db_config = {}
    if sysadmin_config_table is None:
        init(model)

    table = SysadminConfig.get(active_config=True)
    mapped_table = class_mapper(table.__class__).mapped_table

    for key in mapped_table.c.keys():
        db_config[key] = getattr(table, key)

    return db_config