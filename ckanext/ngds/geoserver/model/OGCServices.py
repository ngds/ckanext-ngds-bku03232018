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

    def get_service_url(self, method='Get'):
        return self.wms.getOperationByName('GetMap').methods[method]['url']

    def get_format_options(self, format='image/png'):
        formats = self.wms.getOperationByName('GetMap').formatOptions
        if format in formats:
            return format
        else:
            return formats

    def get_srs(self, layer, srs='EPSG:4326'):
        this_layer = self.wms[layer]
        srs_list = this_layer.crsOptions
        if srs in srs_list:
            return srs
        else:
            return "SRS Not Found"

    def get_bbox(self, layer):
        this_layer = self.wms[layer]
        return this_layer.boundingBoxWGS84

    def do_layer_check(self, data_dict):
        layer_list = list(self.wms.contents)
        resource = data_dict.get("resource", {})
        this_layer = resource.get("layer")
        try:
            first_layer = layer_list[0]
            if this_layer in layer_list:
                return this_layer
            elif this_layer.lower() in layer_list:
                return this_layer.lower()
            else:
                return first_layer
        except Exception:
            pass

    def get_layer_info(self, data_dict):
        layer = self.do_layer_check(data_dict)
        bbox = self.get_bbox(layer)
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

class HandleWFS():

    def __init__(self, url, version="1.0.0"):
        self.wfs = WebFeatureService(url, version=version)
        self.type = self.wfs.identification.type
        self.version = self.wfs.identification.version
        self.title = self.wfs.identification.title
        self.abstract = self.wfs.identification.abstract

    def do_layer_check(self, data_dict):
        layer_list = list(self.wfs.contents)
        resource = data_dict.get("resource", {})
        this_layer = resource.get("layer")
        try:
            first_layer = layer_list[0]
            if this_layer in layer_list:
                return this_layer
            elif this_layer.lower() in layer_list:
                return this_layer.lower()
            else:
                return first_layer
        except Exception:
            pass

    def build_url(self, typename=None, method='{http://www.opengis.net/wfs}Get',
                  operation='{http://www.opengis.net/wfs}GetFeature'):
        service_url = self.wfs.getOperationByName(operation).methods[method]['url']
        request = {'service': 'WFS', 'version': self.version}
        try:
            assert len(typename) > 0
            request['typename'] = ','.join([typename])
        except Exception:
            request['typename'] = ','.join('ERROR_HERE')
            pass
        encoded_request = "&".join("%s=%s" % (key,value) for (key,value) in request.items())
        url = service_url + encoded_request
        return url

    def make_geojson(self, data_dict):
        geojson = []
        type_name = self.do_layer_check(data_dict)
        wfs_url = self.build_url(type_name)
        source = ogr.Open(wfs_url)
        layer = source.GetLayerByIndex(0)
        for feature in layer:
            geojson.append(feature.ExportToJson(as_object=True))
        return geojson

    def make_recline_json(self, data_dict):
        recline_json = []
        geojson = self.make_geojson(data_dict)
        for i in geojson:
            properties = i['properties']
            properties.update(dict(geometry=i['geometry']))
            recline_json.append(properties)
        return recline_json