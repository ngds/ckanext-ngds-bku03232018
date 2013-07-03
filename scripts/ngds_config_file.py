import ConfigParser
import os

# Add .ini parameters that should be set here as (key, value)
params_to_set = [
    ("geoserver.rest_url", "http://localhost:8080/geoserver/rest"),
    ("geoserver.workspace_name", "ngds"),
    ("geoserver.workspace_uri", "http://localhost:5000/ngds")
]

# This builds the config file
cwd = os.getcwd()
dir = os.path.abspath(os.path.join("cwd", "..", "..", "..", "ckan"))
config_file = os.path.join(dir, "development.ini")

if not os.path.exists(config_file):
    print "Could not find development.ini"

else:
    config = ConfigParser.RawConfigParser()
    config.read(config_file)

    print config.sections()

    for param in params_to_set:
        config.set("app:main", param[0], param[1])

    with open(os.path.join(dir, "ngds.ini"), "w") as new_config:
        config.write(new_config)

