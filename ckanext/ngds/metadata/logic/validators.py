import json
from ckanext.ngds.common import pylons_i18n as _

def is_valid_json(key, data, errors, context):
    """
    Checks that a string can be parsed as JSON.

    @param key:
    @param data:
    @param errors:
    @param context:
    @return: None
    """

    try:
        json.loads(data[key])
    except:
        errors[key].append(_('Must be JSON serializable'))

def is_usgin_valid_data():
    pass