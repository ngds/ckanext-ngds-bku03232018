from configobj import ConfigObj
import sys
import os
import argparse

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
    ("ngds.facets_config", "/home/ubuntu/ckanenv/src/ckanext-ngds/facet-config.json"),
    ("ngds.default_group_name", "public"),    
    ("ngds.resources_dir", "/home/ubuntu/ckanenv/src/ckanext-ngds/ckanext/ngds/base/resources"),
    ("ngds.contributors_config", "/home/ngds/pyenv2/src/ckanext-ngds/contributors_config.json"),
    ("extra_public_paths", "/home/ngds/extrapublic/"),
    ("ckan.i18n_directory", "/home/ngds/pyenv2/src/ckanext-ngds")
]

node_params = [
    ("ngds.deployment", "node"),
    ("ngds.full_text_indexing", "true"),
    ("geoserver.rest_url", "http://localhost:8080/geoserver/rest","This is Geoserver rest URL"),
    ("geoserver.workspace_name", "ngds","Geoserver Workspace Name"),
    ("geoserver.workspace_uri", "http://localhost:5000/ngds","Geoserver Workspace URI"),
    ("ngds.bulk_upload_dir", "/home/ngds/work/bulkupload/"),
    ("ngds.client_config_file", "/home/ngds/pyenv2/src/ckanext-ngds/ckanclient.cfg")    
]

central_params = [
    ("ngds.deployment", "central"),
    ("ngds.home_images_dir", "assets"),
    ("ngds.logo_text", "CONTRIBUTING GEOTHERMAL DATA"),
    ("ngds.home_images_config_path", "/home/ngds/pyenv2/src/ckanext-ngds/home_images.cfg")    
]

parser = argparse.ArgumentParser(description='Load NGDS configuration properties')
parser.add_argument('-f','--filename', help='Config File to be updated(Full file Path)', required=True)
parser.add_argument('-d','--deployment', help='Deployment type of NGDS. node/central', required=True)
args = parser.parse_args()


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
    else:
        deployment_params = node_params

    for param in deployment_params:
        config["app:main"][param[0]] = param[1]
        config["app:main"].comments[param[0]] = ["","# %s"%param[2]] if len(param)>2 else []

    config.write()