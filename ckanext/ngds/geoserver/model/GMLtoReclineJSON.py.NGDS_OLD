from lxml import etree
from collections import OrderedDict
import json
import re
from osgeo import ogr

class GMLtoReclineJS():
    def __init__(self):
        return None

    def getElementName(self, element):
        tagname = re.compile("({(?P<ns>.*)})?(?P<element>.*)")
        target = tagname.search(element.tag).groupdict()
        return target["element"]

    def getResourceLayerName(self, data_dict):
        layer_name = data_dict["resource"]["layer_name"]
        lyr_split = re.compile("(?P<datastore>.*):(?P<layer>.*)")
        target = lyr_split.search(layer_name).groupdict
        return target

    def getWorkSpace(self, data_dict):
        data = data_dict
        target = self.getResourceLayerName(data)
        return target()["datastore"]

    def getLayerName(self, data_dict):
        data = data_dict
        target = self.getResourceLayerName(data)
        return target()["layer"]

    def makeGetWFSURL(self, data_dict):
        data = data_dict
        base_url = data["resource"]["url"]
        base_url = base_url.split("/w")[0]
        layer_name = data["resource"]["layer_name"]
        dataStore = self.getWorkSpace(data)
        url = base_url
        url += "/" + dataStore.lower() + "/"
        url += "ows?service=WFS&version=1.0.0&request=GetFeature&typeName="
        url += layer_name.lower()
        print url
        return url

    def makeGetWMSURL(self, data_dict):
        data = data_dict
        base_url = data["resource"]["url"]
        url = base_url.split("?")[0]
        return url

    def getGML(self, url):
        tree = etree.parse(url)
        root = tree.getroot()
        return root

    def MakeReclineJSON(self, data_dict):
        json_obj = []
        attribs = []
        data = data_dict
        gml_wfs = self.makeGetWFSURL(data)
        source = ogr.Open(gml_wfs)
        layer = source.GetLayerByIndex(0)

        for feature in layer:
            json_obj.append(feature.ExportToJson(as_object=True))

        for i in json_obj:
            properties = i['properties']
            properties.update(dict(geometry=i['geometry']))
            attribs.append(properties)

        return attribs