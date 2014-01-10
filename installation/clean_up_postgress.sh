#!/bin/bash

sudo -u postgres dropdb ckan_default
sudo -u postgres dropdb datastore_default
sudo -u postgres dropuser ckan_default
sudo -u postgres dropuser datastore_default

