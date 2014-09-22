import json
import iso8601

from ckanext.ngds.common import pylons_config as config
from ckanext.ngds.common import plugins as p

from ckanext.ngds.common import model as model
from ckanext.ngds.common import dictization as dictization
from ckanext.ngds.common import base as base
from sqlalchemy import desc


def data_publish_enabled():
    value = config.get('ngds.publish', True)
    value = p.toolkit.asbool(value)
    return value

def data_harvest_enabled():
    value = config.get('ngds.harvest', True)
    value = p.toolkit.asbool(value)
    return value

def metadata_edit_enabled():
    value = config.get('ngds.edit_metadata', True)
    value = p.toolkit.asbool(value)
    return value

def get_featured_data():
    value = config.get('ngds.featured_data', None)
    if value:
        value = json.loads(value)
    return value

def get_recent_activity():
    context = {'model': model, 'session': model.Session, 'user': base.c.user}
    activity_objects = model.Session.query(model.Activity)\
        .join(model.Package, model.Activity.object_id == model.Package.id)\
        .filter(model.Activity.activity_type == 'new package')\
        .order_by(desc(model.Activity.timestamp)).limit(3).all()
    activity_dicts = dictization.model_dictize\
        .activity_list_dictize(activity_objects, context)
    return activity_dicts

def get_formatted_date(timestamp):
    return iso8601.parse_date(timestamp).strftime("%B %d, %Y")