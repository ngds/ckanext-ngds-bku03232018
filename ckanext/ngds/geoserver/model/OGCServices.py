''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService
from osgeo import ogr
from ckan.plugins import toolkit

class HandleWMS():

    def __init__(self, url, version="1.1.1"):
        self.wms = WebMapService(url, version=version)
        self.type = self.wms.identification.type
        self.version = self.wms.identification.version
        self.title = self.wms.identification.title
        self.abstract = self.wms.identification.abstract
        self.size = (256, 256)

    def get_service_operations(self):
        wms = self.wms.operations
        return [op.name for op in wms]

    def get_service_url(self, method='Get'):
        return self.wms.getOperationByName('GetMap').methods[method]['url']

    def get_format_options(self, format='image/png'):
        formats = self.wms.getOperationByName('GetMap').formatOptions
        if format in formats:
            return format
        else:
            return formats

    def get_srs(self, layer, srs='EPSG:4326'):
        thisLayer = self.wms[layer]
        srsList = thisLayer.crsOptions
        if srs in srsList:
            return srs
        else:
            return "SRS Not Found"

    def do_layer_check(self, data_dict):
        layers = list(self.wms.contents)
        pkg_id = data_dict.get("pkg_id")
        pkg = toolkit.get_action("package_show")(None, {'id': pkg_id})
        resource = pkg.get('resources')
        try:
            first_layer = layers[0]
            if 'layer_name' in resource:
                if resource.get('layer_name') in layers:
                    return resource.get('layer_name')
            else:
                return first_layer
        except Exception:
            pass

    def get_layer_info(self, layer):
        bbox = layer.boundingBoxWGS84
        srs = self.get_srs(layer)
        format = self.get_format_options()
        service_url = self.get_service_url()
        return {
            'layer': layer,
            'bbox': bbox,
            'srs': srs,
            'format': format,
            'service_url': service_url
        }

url = 'http://kyanite/ArcGIS/services/aasggeothermal/TXActiveFaults/MapServer/WMSServer'

a = HandleWMS(url)
b = a.get_service_operations()
c = a.get_service_methods()
print b
print c