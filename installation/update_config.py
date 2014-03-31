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

from configobj import ConfigObj
import sys
import os
import argparse

"""
Updates the config file based on the inputs(key, value)
If the value needs to be appended then specify (-a) otherwise by default value will be overwritten.
Comments can be updated by passing '-c' parameter. Enclose the comments value with quotes.
"""

parser = argparse.ArgumentParser(description='Config File Updater')
parser.add_argument('-f','--filename', help='Config File to be updated(Full file Path)', required=True)
parser.add_argument('-s','--section', help='Section of file to look for key (ex. [app:main])', default='app:main')
parser.add_argument('-a','--append', help='Specify if needs to be appended with existing value', action='store_true')
parser.add_argument('-k','--key', help='Config File Key to be added/updated', required=True)
parser.add_argument('-v','--value', help='Value of the key', required=True)
parser.add_argument('-c','--comments', help='Comments for the configuration key.(Enclose with quotes for using space).')
args = parser.parse_args()


if not os.path.exists(args.filename):
    print "Could not find config file: %s" % args.filename
else:
    config = ConfigObj(args.filename)
    old_value = config[args.section].get(args.key)

    new_value = args.value if not args.append else old_value+" "+args.value

    config[args.section][args.key] = new_value
    if args.comments:
        config[args.section].comments[args.key] = ["","# %s"%args.comments]

    config.write()
