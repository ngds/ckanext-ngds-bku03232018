from ckanext.ngds.common import pylons_config as config
from ckanext.ngds.common import plugins as p

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