''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

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
parser.add_argument('-a','--append', help='Specify if needs to be appended with existing value', action='store_true')
parser.add_argument('-k','--key', help='Config File Key to be added/updated', required=True)
parser.add_argument('-v','--value', help='Value of the key', required=True)
parser.add_argument('-c','--comments', help='Comments for the configuration key.(Enclose with quotes for using space).')
args = parser.parse_args()


if not os.path.exists(args.filename):
    print "Could not find config file: %s" % args.filename
else:
    config = ConfigObj(args.filename)
    old_value = config["app:main"].get(args.key)

    new_value = args.value if not args.append else old_value+" "+args.value

    config["app:main"][args.key] = new_value
    if args.comments:
        config["app:main"].comments[args.key] = ["","# %s"%args.comments]

    config.write()
