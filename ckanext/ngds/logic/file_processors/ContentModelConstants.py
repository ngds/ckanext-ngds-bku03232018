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


class ContentModelValue(object):
    def __init__(self, cm, cmv):
        self.cm = cm
        self.cmv = cmv

    def __hash__(self):
        det = self.cm + self.cmv
        hash = 0
        for c in det:
            hash = 101 * hash + ord(c)
        return hash

    def __eq__(self, other):
        return self.cm == other.cm and self.cmv == other.cmv


BHT_1_5 = ContentModelValue('http://schemas.usgin.org/uri-gin/ngds/dataschema/boreholetemperature/',
                            'http://schemas.usgin.org/uri-gin/ngds/dataschema/boreholetemperature/1.5')
