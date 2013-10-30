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


def hottest_well_temp(fp):
    hwt = 0
    for row in fp:
        if hwt < row['MaximumRecordedTemperature']:
            hwt = row['MaximumRecordedTemperature']
    return hwt


def coolest_well_temp(fp):
    cwt = 0
    init_v = 0
    for row in fp:
        if init_v == 0:
            cwt = row['MaximumRecordedTemperature']
        if cwt > row['MaximumRecordedTemperature'] and row['MaximumRecordedTemperature'] != 0:
            cwt = row['MaximumRecordedTemperature']
    return cwt