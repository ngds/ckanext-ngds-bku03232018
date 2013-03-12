#!/bin/bash
# test.sh

dbuser="ckanuser"
db="ngdstest" 

#Create a test database
sudo su postgres -c "psql -c 'CREATE DATABASE $db OWNER $dbuser'" 

#Run nose tests
cd ~/pyenv/src/ckanext-ngds
~/pyenv/bin/nosetests --ckan --with-pylons=test-core.ini

#Drop the test database
sudo su postgres -c "psql -c 'DROP DATABASE $db'" 
