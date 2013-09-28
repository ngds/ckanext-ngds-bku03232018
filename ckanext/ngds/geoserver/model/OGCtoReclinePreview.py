from owslib.wms import WebMapService

#url = "http://geo.cei.psu.edu:8080/geoserver/wms"
#layer = "cei:precip_2009_0"
#version = "1.1.1"
#srs = "EPSG:4326"
#format = "image/png"

class DataServiceToReclineJS():

	def __init__(self, url, version):
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

	def get(self, layer):
		thisFormat = self.get_service_format_options(format)
		layer_details = self.get_layer_details(layer)
		img = self.wms.getmap(	layers=[layer],
								srs=layer_details['srs'],
								bbox=layer_details['bbox'],
								size=self.size,
								format=thisFormat)
		return img.url

#a = DataServiceToReclineJS(url, version)
#print a.get(layer)