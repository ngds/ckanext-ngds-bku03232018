from lxml import etree
from collections import OrderedDict
import json
import re

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

    def makeGetFeatureURL(self, data_dict):
        data = data_dict
        base_url = data["resource"]["url"]
        base_url = base_url.split("/w")[0]
        layer_name = data["resource"]["layer_name"]
        dataStore = self.getWorkSpace(data)
        url = base_url
        url += "/" + dataStore + "/"
        url += "ows?service=WFS&version=1.0.0&request=GetFeature&typeName="
        url += "NGDS:activefaults" #layer_name
        return url

    def getGML(self, url):
        tree = etree.parse(url)
        root = tree.getroot()
        return root

    def MakeReclineJSON(self, data_dict):
        data = data_dict
        url = self.makeGetFeatureURL(data)
        ws = self.getWorkSpace(data)
        lyr = "activefaults" #self.getLayerName(data)
        gml = self.getGML(url)
        attributes = []
        valid_geometry = ["Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon"]
        nsmap = gml.nsmap
        if None in nsmap.keys():
            del nsmap[None]
        try:
            leaves = gml.xpath("//" + ws + ":" + lyr, namespaces=nsmap)
            for maple in leaves:
                fid = maple.attrib["fid"]
                geometryType = [self.getElementName(twig.find("gml:" + valid, namespaces=nsmap)) for twig in maple for valid in valid_geometry if twig.find("gml:" + valid, namespaces=nsmap) is not None]
                properties = [(self.getElementName(twig),twig.text) for twig in maple]
                properties.insert(0, ("field_id",fid))
                geometry_coords = [twig.find("gml:" + valid + "/gml:coordinates", namespaces=nsmap).text for twig in maple for valid in valid_geometry if twig.find("gml:" + valid + "/gml:coordinates", namespaces=nsmap) is not None]
                geom_coordinates = geometry_coords[0].split(" ")
                coordinates = [[float(x) for x in q.split(",")] for q in geom_coordinates]
                data = {}
                data.update(dict(type=geometryType[0],coordinates=coordinates))
                properties.insert(len(properties),("geometry", data))
                attributes.append(OrderedDict(properties))
        except:
            pass
        return json.dumps(attributes)