''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

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