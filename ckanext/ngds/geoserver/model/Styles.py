from geoserver.catalog import Catalog
from pylons import config as ckan_config

"""
Notes for tomorrow:

cat = Catalog("http://localhost:8080/geoserver/rest", "admin", "geoserver")
[style.name for style in cat.get_styles()]
cat.create_style("heatflow", open("HeatFlow.sld").read())
"""