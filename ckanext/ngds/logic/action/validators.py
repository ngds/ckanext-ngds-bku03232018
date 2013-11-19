''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

from pylons.i18n import _
from ckan.plugins import toolkit as tk
import json, datetime

"""
A validation function has a signature that looks like this:

    not_missing(key, data, errors, context):

... where `key` is the name of the key being validated, `data` is the entire package dictionary, `errors` is a
dictionary of errors, and `context` is CKAN `context` as usual.

These functions can do a few things:

1. Make adjustments to the Package by manipulating the `data` dictionary
2. Add errors to the `errors` dictionary. Generally the key in the error dictionary is the field name, and the
 value should be the error message, ideally internationalized
3. Raise a `Invalid` exception, which marks the resource as invalid and halts validation.
4. Raise a `StopOnError` exception, which stops the validator from running any more of the validation functions
 for a particular field
"""

def has_fifty_characters(key, data, errors, context):
    """Makes sure that a field's content has at least 50 characters"""
    value = data[key]

    if len(value) < 50:
        errors[key].append(_('Field must have at least 50 characters'))

def apply_default_org(key, data, errors, context):
    """A Package's organization must always be `public`"""
    data[key] = 'public'

def is_valid_json(key, data, errors, context):
    """Checks that a string can be parsed as JSON"""
    try:
        json.loads(data[key])
    except:
        errors[key].append(_('Must be JSON serializable'))

def is_valid_contact(key, data, errors, context):
    """Check if a key's value is a valid NGDS contact. Assumes you've already ran it through `is_valid_json`"""
    value = json.loads(data[key])
    keys = value.keys()

    if len(keys) != 2 or 'name' not in keys or 'email' not in keys:
        errors[key].append(_('Not a valid NGDS contact'))

def is_valid_list_of_contacts(key, data, errors, context):
    """Check if a key's value is a valid JSON list of NGDS contacts. Assumes you've already ran it through `is_valid_json`"""
    value = json.loads(data[key])

    if not isinstance(value, list):
        errors[key].append(_('Not a valid list of NGDS contacts'))
        return

    for c in value:
        keys = c.keys()
        if len(keys) != 2 or 'name' not in keys or 'email' not in keys:
            errors[key].append(_('Not a valid NGDS contact'))

def is_valid_rectangle(key, data, errors, context):
    """Makes sure that the given key's value is a valid rectangle in GeoJSON. Assumes you've already ran it through `is_valid_json`"""
    value = json.loads(data[key])
    valid = True

    try:
        if value['type'] != 'Polygon': valid = False
        if len(value['coordinates']) != 5: valid = False
        if value['coordinates'][0] != value['coordinates'][4]: valid = False
    except:
        valid = False

    if not valid:
        errors[key].append(_('Not a valid bounding box'))

def is_in_list(list_of_values):
    """Check if a key's value is in a set of values"""

    def callable(key, data, errors, context):
        value = data[key]
        if value not in list_of_values:
            errors[key].append(_('Must be one of %s' % ", ".join(list_of_values)))

    return callable

def is_valid_date(key, data, errors, context):
    """Makes sure that a value is a valid ISO 8601 date"""

    def date_str_to_datetime(date_str):
        '''Convert ISO-like formatted datestring to datetime object.

        This function converts ISO format date- and datetime-strings into
        datetime objects.  Times may be specified down to the microsecond.  UTC
        offset or timezone information may **not** be included in the string.

        Note - Although originally documented as parsing ISO date(-times), this
               function doesn't fully adhere to the format.  This function will
               throw a ValueError if the string contains UTC offset information.
               So in that sense, it is less liberal than ISO format.  On the
               other hand, it is more liberal of the accepted delimiters between
               the values in the string.  Also, it allows microsecond precision,
               despite that not being part of the ISO format.
        '''

        time_tuple = re.split('[^\d]+', date_str, maxsplit=5)

        # Extract seconds and microseconds
        if len(time_tuple) >= 6:
            m = re.match('(?P<seconds>\d{2})(\.(?P<microseconds>\d{6}))?$',
                         time_tuple[5])
            if not m:
                raise ValueError('Unable to parse %s as seconds.microseconds' %
                                 time_tuple[5])
            seconds = int(m.groupdict().get('seconds'))
            microseconds = int(m.groupdict(0).get('microseconds'))
            time_tuple = time_tuple[:5] + [seconds, microseconds]

        return datetime.datetime(*map(int, time_tuple))

    value = data[key]

    if isinstance(value, datetime.datetime):
        return value
    if value == '':
        return None
    try:
        date = date_str_to_datetime(value)
    except (TypeError, ValueError), e:
        raise Invalid(_('Date format incorrect'))
    return date

