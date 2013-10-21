#!/bin/bash
# test.sh

# ___NGDS_HEADER_BEGIN___
#
# National Geothermal Data System - NGDS
# https://github.com/ngds
#
# File: <filename>
#
# Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey
#
# Please Refer to the README.txt file in the base directory of the NGDS
# project:
# https://github.com/ngds/ckanext-ngds/README.txt
#
# ___NGDS_HEADER_END___

dbuser="ckanuser"
db="ngdstest" 

#Create a test database
sudo su postgres -c "psql -c 'CREATE DATABASE $db OWNER $dbuser'" 

#Run nose tests
cd ~/pyenv/src/ckanext-ngds
nosetests --ckan --with-pylons=test-core.ini

#Drop the test database
sudo su postgres -c "psql -c 'DROP DATABASE $db'" 
