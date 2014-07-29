import ckan.plugins as p
import ckanext.ngds.sysadmin.db as db
from ckanext.ngds.common import df

def _sysadmin_config_update(context, data_dict):
    pass

def sysadmin_config_update(context, data_dict):
    try:
        p.toolkit.check_access('sysadmin_config_update', context, data_dict)
    except:
        p.toolkit.abort(401, p.toolkit._('Not authorized to update config'))
    return _sysadmin_config_update(context, data_dict)