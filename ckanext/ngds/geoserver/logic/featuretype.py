from collections import OrderedDict
import json
import ckanext.datastore.db as db
from geoserver.catalog import Layer

class SqlFeatureTypeDef:

    def __init__(self, context, data_dict):
        
        baseGeoserverUrl = data_dict['geoserver']
        resource_id = data_dict['resource_id']
        layer_name = data_dict['layer_name']
        workspace_name = data_dict['workspace_name']
        
        if baseGeoserverUrl is None:
            print "using default geoserver :"+baseGeoserverUrl
            baseGeoserverUrl = 'http://localhost:8080/geoserver/rest/'
        
        # gets the fields of the resource_id in the database URl defined in
        # the context['connection']
        print ">>>>>>>>>>>>> reading field list >>>>>>>>>>>>>>>>>"
        fields = db._get_fields(context, data_dict)   
        print ">>>>>>>>>>>>> done reading field list >>>>>>>>>>>>>>>>>"
         
        self.name = layer_name
        self.title = layer_name
        
        # adds ""s in the field names putting them in another list
        self.fieldNames = [ "\"%s\"" % fld for fld in fields if fld not in ["id", "owningmap"] ]
        #print "fieldNames = "+fieldNames
        
        
        print ">>>>>>>>>>>>> building namespace >>>>>>>>>>>>>>>>>"
        self.namespace = {
            "name": workspace_name,
            "href": baseGeoserverUrl + "/namespaces/" + workspace_name + ".json"                  
        }
        
        
        #self.nativeCRS = layer.srs.wkt
        self.nativeCRS = 'EPSG:4326'
        
        print ">>>>>>>>>>>>> setting bounding box >>>>>>>>>>>>>>>>>"
        
        ''' 
        self.nativeBoundingBox = {
            "minx": layer.extent.min_x,
            "maxx": layer.extent.max_x,
            "miny": layer.extent.min_y,
            "maxy": layer.extent.max_y,
            "crs": "EPSG:" + str(layer.srs.srid)                          
        }
        '''
        
        self.nativeBoundingBox = {
            "minx": '0',
            "maxx": '0',
            "miny": '0',
            "maxy": '0',
            "crs": 'EPSG:4326'                          
        }
        
        
        print ">>>>>>>>>>>>> building geometry >>>>>>>>>>>>>>>>>"
        self.geometry = OrderedDict()
        self.geometry["name"] = "shape"
        self.geometry["type"] = 'shape'
        self.geometry["srid"] = 'EPSG:4326'
        
        print ">>>>>>>>>>>>> building virtual table >>>>>>>>>>>>>>>>>"
        self.virtualTable = OrderedDict()
        self.virtualTable["name"] = self.name
        self.virtualTable["sql"] = "select " + ", ".join(self.fieldNames) + " from " + resource_id 
        self.virtualTable["geometry"] = self.geometry
        
        print ">>>>>>>>>>>>> building store >>>>>>>>>>>>>>>>>"
        self.store = {
            "@class": "dataStore",
            "name": "datastore",
            "href": baseGeoserverUrl + "/workspaces/" + workspace_name + "/datastores/postgis.json"              
        }
        
    def serialize(self):
        return json.dumps({
            "featureType": {
                "name": self.name,
                "title": self.title,
                "namespace": self.namespace,
                "nativeCRS": self.nativeCRS,
                "nativeBoundingBox": self.nativeBoundingBox,
                "metadata": {
                    "entry": {
                        "@key": "JDBC_VIRTUAL_TABLE",
                        "virtualTable": self.virtualTable          
                    }             
                },
                "store": self.store                
            }              
        })