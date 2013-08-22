import ConfigParser
import os

# Add .ini parameters that should be set here as (key, value)
params_to_set = [
    ("geoserver.rest_url", "http://localhost:8080/geoserver/rest"),
    ("geoserver.workspace_name", "ngds"),
    ("geoserver.workspace_uri", "http://localhost:5000/ngds"),
    ("ckan.extra_resource_fields", "parent_resource distributor layer_name content_model_version content_model_uri"),
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
    ("ngds.deployment", "node"),
    ("ngds_resources_dir", "/home/ubuntu/ckanenv/src/ckanext-ngds/ckanext/ngds/base/resources"),
    ("ngds.home_images_dir", "assets"),
    ("ngds.home_images_config_path", "/home/ngds/pyenv2/src/ckanext-ngds/home_images.cfg")
]

# This builds the config file
cwd = os.getcwd()
ckan_dir = os.path.abspath(os.path.join(cwd, "..", "..", "ckan"))
config_file = os.path.join(ckan_dir, "development.ini")

if not os.path.exists(config_file):
    print "Could not find development.ini"

else:
    config = ConfigParser.RawConfigParser()
    config.read(config_file)

    print config.sections()

    for param in params_to_set:
        config.set("app:main", param[0], param[1])

    with open(os.path.join(ckan_dir, "ngds.ini"), "w") as new_config:
        config.write(new_config)

