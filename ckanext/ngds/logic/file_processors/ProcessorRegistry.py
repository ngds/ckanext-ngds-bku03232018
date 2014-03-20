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

__author__ = 'kaffeine'

from ckanext.ngds.logic.file_processors.ContentModelConstants import ContentModelValue, BHT_1_5
import ckanext.ngds.logic.file_processors.CSVProcessors as CSVP


def get_registry():
    return {
        BHT_1_5: [
            {'metadata_field': 'hottest_well_temp', 'func': CSVP.hottest_well_temp},
            {'metadata_field': 'coolest_well_temp', 'func': CSVP.coolest_well_temp}
        ]
    }
