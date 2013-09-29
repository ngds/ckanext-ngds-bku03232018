from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService

#url = "http://geo.cei.psu.edu:8080/geoserver/wms"
#layer = "cei:precip_2009_0"
#version = "1.1.1"
#srs = "EPSG:4326"
#format = "image/png"

class WMSDataServiceToReclineJS():

    def __init__(self, url, version="1.1.1"):
        self.wms = WebMapService(url, version=version)
        self.type = self.wms.identification.type
        self.version = self.wms.identification.version
        self.title = self.wms.identification.title
        self.abstract = self.wms.identification.abstract
        self.size = (256, 256)

    def get_layers(self):
        return list(self.wms.contents)

    def get_srs(self, layer, srs):
        thisSRS = srs
        thisLayer = self.wms[layer]
        srsList = thisLayer.crsOptions
        if thisSRS in srsList:
            return thisSRS
        else:
            return thisSRS + " not found"

    def get_service_operations(self):
        thisWMS = self.wms.operations
        return [op.name for op in thisWMS]

    def get_service_methods(self):
        thisWMS = self.wms.getOperationByName('GetMap').methods
        return thisWMS

    def get_GET_url(self):
        methods = self.get_service_methods()
        return methods['Get']['url']

    def get_service_format_options(self, format):
        thisFormat = format
        thisWMS = self.wms.getOperationByName('GetMap').formatOptions
        if thisFormat in thisWMS:
            return thisFormat
        else:
            return thisFormat + " not found"

    def get_layer_details(self, layer):
        keys = ['layer', 'bbox', 'srs', 'format']
        thisLayer = self.wms[layer]
        bbox = thisLayer.boundingBoxWGS84
        thisSRS = self.get_srs(layer, srs)
        return dict(zip(keys,[thisLayer,bbox,thisSRS,'none']))

    def get_service_url(self, layer):
        thisFormat = self.get_service_format_options(format)
        layer_details = self.get_layer_details(layer)
        serviceURL = self.wms.getmap(	layers=[layer],
                                srs=layer_details['srs'],
                                bbox=layer_details['bbox'],
                                size=self.size,
                                format=thisFormat)
        return serviceURL.url

    def hack_up_a_layer_name(self, data_dict):
        data = data_dict.get("resource")
        if data.get("layer_name"):
            print data.get("layer_name")
            return data.get("layer_name")
        elif data.get("layer"):
            print data.get("layer")
            return data.get("layer")
        elif data.get("layers"):
            print data.get("layers")
            return data.get("layers")
        else:
            try:
                layer_list = self.get_layers()
                print layer_list[0]
                return layer_list[0]
            except:
                return "Sorry, can't find a layer!"

    def recline_ogc_wms(self, data_dict):
        data = data_dict
        keys = ["layer", "url"]
        layer = self.hack_up_a_layer_name(data)
        url = self.get_GET_url()
        return dict(zip(keys,[layer,url]))

class WFSDataServiceToReclineJS():

    def __init__(self, url, version="1.0.0"):
        self.wfs = WebFeatureService(url, version=version)
        self.type = self.wfs.identification.type
        self.version = self.wfs.identification.version
        self.title = self.wfs.identification.title
        self.abstract = self.wfs.identification.abstract

#a = DataServiceToReclineJS(url, version)
#print a.get_service_url(layer)