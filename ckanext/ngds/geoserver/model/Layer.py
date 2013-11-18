''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

from geoserver.support import url
from ckanext.ngds.geoserver.model.Geoserver import Geoserver
from ckanext.ngds.geoserver.model.Datastored import Datastored
from ckanext.ngds.geoserver.model.ShapeFile import Shapefile
from ckan.plugins import toolkit
from pylons import config
import json

class Layer(object):

    @classmethod
    def publish(cls, package_id, resource_id, layer_name, username, geoserver=Geoserver.from_ckan_config(), lat_field=None, lng_field=None):
        l = cls(package_id, resource_id, layer_name, username, geoserver, lat_field, lng_field)
        if l.create():
            return l
        else:
            return None

    def __init__(self, package_id, resource_id, layer_name, username, geoserver=Geoserver.from_ckan_config(), lat_field=None, lng_field=None):
        self.geoserver = geoserver
        self.store = geoserver.default_datastore()
        self.name = layer_name
        self.username = username
        self.file_resource = toolkit.get_action("resource_show")(None, {"id": resource_id})
        self.package_id = package_id
        self.resource_id = resource_id

        # Spatialize it
        url = self.file_resource["url"]
        kwargs = {"resource_id": self.file_resource["id"]}

        if url.endswith('.zip'):
            cls = Shapefile
        elif url.endswith('.csv'):
            cls = Datastored
            kwargs.update({
                "lat_field": lat_field,
                "lng_field": lng_field
            })
        else:
            # The resource cannot be spatialized
            raise Exception(toolkit._("Only CSV and Shapefile data can be spatialized"))

        self.data = cls(**kwargs)

        # Spatialize
        if not self.data.publish():
            # Spatialization failed
            raise Exception(toolkit._("Spatialization failed."))

    def create(self):
        """
        Creates the new layer to Geoserver and then creates the resources in Package(CKAN).
        """

        self.create_layer()
        self.create_geo_resources()

        return True

    def remove(self):
        """
        Removes the Layer from Geoserver and the geo resources from the pacakage.
        """

        self.remove_layer()
        self.remove_geo_resources()

    def create_layer(self):
        """
        Constructs the layer details and creates it in the geoserver.
        If the layer already exists then return the pre-existing layer.
        Layer "existence" is based entirely on the layer's name -- it must be unique

        @returns geoserver layer
        """

        # If the layer already exists in Geoserver then return it

        layer = self.geoserver.get_layer(self.name)

        if not layer:
            #Construct layer creation request.
            feature_type_url = url(self.geoserver.service_url, [
                "workspaces",
                self.store.workspace.name,
                "datastores",
                self.store.name,
                "featuretypes"
            ])

            data = {
                "featureType": {
                    "name": self.name,
                    "nativeName": self.data.table_name()
                }
            }

            request_headers = {"Content-type": "application/json"}

            response_headers, response = self.geoserver.http.request(
                feature_type_url,
                "POST",
                json.dumps(data),
                request_headers
            )

            if not 200 <= response_headers.status < 300:
                raise Exception(toolkit._("Geoserver layer creation failed: %i -- %s") % (response_headers.status, response))

            layer = self.geoserver.get_layer(self.name)

        # Add the layer's name to the file resource
        self.file_resource.update({"layer_name": self.name})
        self.file_resource = toolkit.get_action("resource_update")({"user": self.username}, self.file_resource)

        # Return the layer
        return layer

    def remove_layer(self):
        """
        Removes the layer from geoserver.
        """
        layer = self.geoserver.get_layer(self.name)
        if layer:
            self.geoserver.delete(layer, purge=True, recurse=True)

        # Remove the layer_name from the file resource
        if self.file_resource.get("layer_name"):
            del self.file_resource["layer_name"]

        self.file_resource = toolkit.get_action("resource_update")({"user": self.username}, self.file_resource)

        return True

    def create_geo_resources(self):
        """
        Creates the geo resources(WMS, WFS) into CKAN. Created layer can provide WMS and WFS capabilities.
        Gets the file resource details and creates two new resources for the package.

        Must hand in a CKAN user for creating things
        """

        context = {"user": self.username}

        # WMS Resource Creation
        data_dict = {
            'url': self.geoserver.service_url.replace("/rest", "/wms?request=GetCapabilities"),
            'package_id': self.package_id,
            'description': 'WMS for %s' % self.file_resource['name'],
            'parent_resource': self.file_resource['id'],
            'distributor': self.file_resource.get("distributor", json.dumps({"name": "Unknown", "email": "unknown"})),
            'protocol': 'OGC:WMS',
            'layer':"%s:%s" % (config.get("geoserver.workspace_name", "NGDS"), self.name),
            'resource_format': 'data-service',
            'format': ''
        }
        if self.file_resource.get("content_model_version") and self.file_resource.get("content_model_uri"):
            data_dict.update({
                "content_model_version": self.file_resource.get("content_model_version"),
                "content_model_uri": self.file_resource.get("content_model_uri")
            })
        self.wms_resource = toolkit.get_action('resource_create')(context, data_dict)

        # WFS Resource Creation
        data_dict.update({
            "package_id": self.package_id,
            "url": self.geoserver.service_url.replace("/rest", "/wfs?request=GetCapabilities"),
            'distributor': self.file_resource.get("distributor", json.dumps({"name": "Unknown", "email": "unknown"})),
            "description": "WFS for %s" % self.file_resource["name"],
            "protocol": "OGC:WFS",
            "layer":"%s:%s" % (config.get("geoserver.workspace_name", "NGDS"), self.name),
            'resource_format': 'data-service',
            'format': ''
        })
        self.wfs_resource = toolkit.get_action('resource_create')(context, data_dict)

        # Return the two resource dicts
        return self.wms_resource, self.wfs_resource

    def remove_geo_resources(self):
        """
        Removes the list of resources from package. If the resources list not provided then find the geo resources based
        on parent_resource value and then removes them from package.
        """

        context = {"user": self.username}
        results = toolkit.get_action("resource_search")(context, {"query": "parent_resource:%s" % self.file_resource["id"]})
        for result in results.get("results", []):
            toolkit.get_action("resource_delete")(context, {"id": result["id"]})
