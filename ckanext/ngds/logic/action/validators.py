""" NGDS_HEADER_BEGIN

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey

Please refer the the README.txt file in the base directory of the NGDS project:
https://github.com/ngds/ckanext-ngds/blob/master/README.txt

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero
General Public License as published by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.  https://github.com/ngds/ckanext-ngds
ngds/blob/master/LICENSE.md or
http://www.gnu.org/licenses/agpl.html

NGDS_HEADER_END """

from pylons.i18n import _
from ckan.plugins import toolkit as tk
import json, datetime, re
from itertools import count
from ckan.lib.navl.dictization_functions import Invalid
from ckan.model import (MAX_TAG_LENGTH, MIN_TAG_LENGTH)

# Content Model utilities
from ckanext.ngds.contentmodel.logic.action import contentmodel_checkFile as check_model_file
from ckanext.ngds.contentmodel.logic.action import contentmodel_list_short as models_list

# Hack to make simple tests work when pylons is not configured
try:
    result = _('translate')
except TypeError:
    def _(s): return s

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
        value = [value]
        data[key] = unicode(json.dumps(value))

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
        if len(value['coordinates'][0]) != 5: valid = False
        if value['coordinates'][0][0] != value['coordinates'][0][4]: valid = False
        data.update({'non-geographic': 'False'})
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

    try:
        date = date_str_to_datetime(value)
    except (TypeError, ValueError), e:
        errors[key].append(_('Date format incorrect'))

def is_valid_model_uri(key, data, errors, context):
    """
    Checks that a uri is valid
    """
    uri = data[key]
    if uri.lower() == 'none':
        pass
    else:
        models = models_list({}, {})
        uris = [cm['uri'] for cm in models]
        if uri not in uris:
            errors[key].append(_('Invalid Content Model URI'))


def is_valid_model_version(key, data, errors, context):
    """
    Checks that a version is valid.
    """
    version = data[key]
    if version.lower() == 'none':
        pass
    else:
        models = dict((cm['uri'], cm) for cm in models_list({}, {}))
        uri = data.get('content_model_uri', '')
        version_number = version.split('/')[-1]
        this_model = models.get(uri, {})
        if version_number not in [v['version'] for v in this_model.get('versions', [])]:
            errors[key].append(_('Invalid Content Model Version'))

def check_uploaded_file(resource, errors, error_key):
    """
    This function appends errors to the error dictionary if an uploaded file does not conform to the specified
    content model. It assumes that the resource_dict has valid model_uri and model_version.
    """
    validation_results = check_model_file({}, {
        "cm_uri": resource["content_model_uri"],
        "cm_version": resource["content_model_version"].split('/')[-1], # field contains the version URI
        "cm_version_url": resource["content_model_version"],
        "cm_resource_url": resource["url"],
        "cm_layer": resource["content_model_layer"]
    })

    if not validation_results['valid']:
        errors[error_key] = list(set(errors.get(error_key, [])) & set(validation_results['messages']))

def is_non_geographic(key, data, errors, context):
    value = data[key]
    if value.lower() == "true" or "false":
        data.update({'spatial': 'None'})
    else:
        errors[key].append(_("Invalid Non-Geographic Value"))

def ngds_tag_name_validator(value, context):

    tagname_match = re.compile('[\w \-.:]*$', re.UNICODE)
    if not tagname_match.match(value):
        raise Invalid(_('Tag "%s" must be alphanumeric characters or symbols: -_.:') % (value))
    return value

def ngds_tag_string_convert(key, data, errors, context):
    '''Takes a list of tags that is a comma-separated string (in data[key])
    and parses tag names. These are added to the data dict, enumerated. They
    are also validated.'''

    if isinstance(data[key], basestring):
        tags = [tag.strip() \
                for tag in data[key].split(',') \
                if tag.strip()]
    else:
        tags = data[key]

    current_index = max( [int(k[1]) for k in data.keys() if len(k) == 3 and k[0] == 'tags'] + [-1] )

    for num, tag in zip(count(current_index+1), tags):
        data[('tags', num, 'name')] = tag

    for tag in tags:
        ngds_tag_length_validator(tag, context)
        ngds_tag_name_validator(tag, context)

def ngds_tag_length_validator(value, context):

    if len(value) < MIN_TAG_LENGTH:
        raise Invalid(('Tag "%s" length is less than minimum %s') % (value, MIN_TAG_LENGTH))
    if len(value) > MAX_TAG_LENGTH:
        raise Invalid(('Tag "%s" length is more than maximum %i') % (value, MAX_TAG_LENGTH))
    return value