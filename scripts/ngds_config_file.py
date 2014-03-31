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


parser = argparse.ArgumentParser(description='Load NGDS configuration properties')
parser.add_argument('-f','--filename', help='Config File to be updated(Full file Path)', required=True)
parser.add_argument('-d','--deployment', help='Deployment type of NGDS. node/central', required=True)
parser.add_argument('-r','--root', help='Path to CKAN NGDS Extension, for example ~/home/ubuntu/ckanenv/src/ckanext-ngds', required=True)
args = parser.parse_args()

# Add .ini parameters that should be set here as (key, value)
params_to_set = [
    ("ckan.extra_resource_fields", "parent_resource distributor layer_name content_model_version content_model_uri","Extra Resources fields"),
    ("ngds.csw.title", "NGDS CSW"),
    ("ngds.csw.abstract", "NGDS is awesome"),
    ("ngds.csw.keywords", "ngds, csw, ogc, catalog"),
    ("ngds.csw.keywords_type", "theme"),
    ("ngds.csw.fees", "None"),
    ("ngds.csw.accessconstraints", "None"),
    ("ngds.csw.provider.name", "Roger Mebowitz"),
    ("ngds.csw.provider.url", "http://geothermaldatasystem.org"),
    ("ngds.csw.contact.name", "Roger Mebowitz"),
    ("ngds.csw.contact.position", "Maintainer"),
    ("ngds.csw.contact.address", "123 Somewhere St."),
    ("ngds.csw.contact.city", "Anywhere"),
    ("ngds.csw.contact.state", "State"),
    ("ngds.csw.contact.zip", "12345"),
    ("ngds.csw.contact.country", "USA"),
    ("ngds.csw.contact.phone", "123-456-7890"),
    ("ngds.csw.contact.fax", "123-456-7890"),
    ("ngds.csw.contact.email", "nothing@false.com"),
    ("ngds.csw.contact.url", "http://geothermaldatasystem.org"),
    ("ngds.csw.contact.hours", "0800h - 1600h EST"),
    ("ngds.csw.contact.instructions", "During hours of service"),
    ("ngds.csw.contact.role", "pointOfContact"),
    ("ngds.facets_config", args.root + "/facet-config.json"),
    ("ngds.default_group_name", "public"),
    ("ngds.resources_dir", args.root + "/ckanext/ngds/base/resources"),
    ("ngds.contributors_config", args.root + "/contributors_config.json"),
    ("extra_public_paths", "/home/ngds/extrapublic/"),
    ("solr_url", "http://localhost:8983/solr"),
    ("ckan.i18n_directory", args.root),
    ("search.facets.limit", "30000")
]

node_params = [
    ("ngds.deployment", "node"),
    ("ngds.full_text_indexing", "true"),
    ("geoserver.rest_url", "geoserver://admin:geoserver@localhost:8080/geoserver/rest","This is Geoserver rest URL"),
    ("geoserver.workspace_name", "ngds","Geoserver Workspace Name"),
    ("geoserver.workspace_uri", "http://localhost:5000/ngds","Geoserver Workspace URI"),
    ("ngds.bulk_upload_dir", "/home/ngds/work/bulkupload/"),
    ("ngds.client_config_file", args.root + "/ckanclient.cfg"),
    ("ckan.site_logo", "/assets/nib.png")
]

node_plugins = 'stats json_preview recline_preview datastore spatial_metadata spatial_query datastorer csw metadata geoserver ngdsui'

central_params = [
    ("ngds.deployment", "central"),
    ("ngds.home_images_dir", "assets"),
    ("ngds.logo_text", "CONTRIBUTING GEOTHERMAL DATA"),
    ("ngds.home_images_config_path", args.root + "/home_images.cfg"),
    ("ckan.site_logo", "/assets/logo.png")
]

central_plugins = 'stats json_preview recline_preview datastore spatial_metadata spatial_query spatial_harvest_metadata_api csw_harvester csw metadata ngds_harvester geoserver ngdsui harvest ckan_harvester'

if not os.path.exists(args.filename):
    print "Could not find config file: %s" % args.filename
else:
    config = ConfigObj(args.filename)

    for param in params_to_set:
        config["app:main"][param[0]] = param[1]
        config["app:main"].comments[param[0]] = ["","# %s"%param[2]] if len(param)>2 else []

    deployment_params = []

    if args.deployment.lower() == 'central':
        deployment_params = central_params
        plugins = central_plugins
    else:
        deployment_params = node_params
        plugins = node_plugins

    for param in deployment_params:
        config["app:main"][param[0]] = param[1]
        config["app:main"].comments[param[0]] = ["","# %s"%param[2]] if len(param)>2 else []

    config["app:main"]["ckan.plugins"] = plugins
    config.write()
