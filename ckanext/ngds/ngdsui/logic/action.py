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

"""
Some actions for making NGDS custom activity streams
"""

import ckan.lib.activity_streams as activity_streams
from ckanext.harvest.model import (HarvestSource, HarvestObject)
from ckan.logic import NotFound
from ckan.logic import get_action

def ngds_harvest_source(context, data_dict):
    '''
    Get some harvest source information for a package.
    '''

    session = context['session']

    dataset_id = data_dict.get('id')

    query = session.query(HarvestSource)\
            .join(HarvestObject)\
            .filter_by(package_id=dataset_id)\
            .order_by(HarvestObject.gathered.desc())
    source = query.first()

    harvest_info = {
        'harvest_title': source['title'],
        'harvest_type': source['type'],
        'harvest_url': source['url']
    }

    if not source:
        raise NotFound

    return harvest_info

def ngds_activities_html(context, data_dict):
    '''
    Return a package's activity stream as HTML.
    The activity stream is rendered as a snippet of HTML meant to be included
    in an HTML page, i.e. it doesn't have any HTML header or footer.
    '''

    harvest = ngds_harvest_source(context, data_dict)

    package_activity_list = get_action('package_activity_list')
    activity_stream = package_activity_list(context, data_dict)
    offset = int(data_dict.get('offset', 0))
    extra_vars = {
        'controller': 'package',
        'action': 'activity',
        'id': data_dict['id'],
        'offset': offset,
        }
    return activity_streams.activity_list_to_html(context, activity_stream,
            extra_vars)
