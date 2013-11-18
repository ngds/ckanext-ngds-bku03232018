''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

import logging
import ckan.logic as logic
from ckanext.ngds.geoserver.model.Geoserver import Geoserver
from ckanext.ngds.geoserver.model.Layer import Layer
from ckan.plugins import toolkit
from ckanext.ngds.env import ckan_model, h, _
from owslib.wms import WebMapService
import socket


log = logging.getLogger(__name__)
_get_or_bust = logic.get_or_bust


def layer_exists(context, data_dict):
    """
    Checks whether layer exists in the geoserver. If not then returns False.

    @return: Boolean
    """

    if 'layer_name' in data_dict:
        layer_name = _get_or_bust(data_dict, 'layer_name')

    geoserver = Geoserver.from_ckan_config()
    if geoserver.get_layer(layer_name) is None:
        return False
    else:
        return True


def publish(context, data_dict):
    """
    Publishes the resource details as Geoserver layer based on the input details.
    If the layer creation is successful then returns "Success" msg, otherwise raises an Exception.
    """

    # Gather inputs
    resource_id = data_dict.get("resource_id", None)
    layer_name = data_dict.get("layer_name", resource_id)
    username = context.get("user", None)
    package_id = data_dict.get("package_id", None)
    lat_field = data_dict.get("col_latitude", None)
    lng_field = data_dict.get("col_longitude", None)
    geoserver_layer_name = data_dict.get("gs_lyr_name", None)

    # Check that you have everything you need
    if None in [resource_id, layer_name, username, package_id]:
        raise Exception(toolkit._("Not enough information to publish resource"))

    # Publish a layer
    def pub():
        if geoserver_layer_name is not None:
            l = Layer.publish(package_id, resource_id, geoserver_layer_name, username, lat_field=lat_field,
                              lng_field=lng_field)
            return l
        else:
            l = Layer.publish(package_id, resource_id, layer_name, username, lat_field=lat_field, lng_field=lng_field)
            return l

    try:
        l = pub()
        if l is None:
            h.flash_error(
                _(
                    "Failed to generate a geoserver layer. Please contact the site administrator if this problem persists."))
            raise Exception(toolkit._("Layer generation failed"))
        else:
            # csv content should be spatialized or a shapefile uploaded, Geoserver updated, resources appended.
            #  l should be a Layer instance. Return whatever you wish to
            h.flash_success(
                _("This resource has successfully been published as an OGC service."))
            return "Success"
    except socket.error:
        h.flash_error(
            _("Error connecting to geoserver. Please contact the site administrator if this problem persists."))


        # Confirm that everything went according to plan


def unpublish(context, data_dict):
    """
    Un-publishes the geoserver layer based on the resource identifier. Retrieves the geoserver layer name and package
     identifier to construct layer and remove it.
    """
    resource_id = data_dict.get("resource_id")
    layer_name = data_dict.get("layer_name")
    layer_name = "NGDS:" + resource_id
    username = context.get('user')
    geoserver_layer_name = data_dict.get("gs_lyr_name", None)
    file_resource = toolkit.get_action("resource_show")(None, {"id": resource_id})

    if not layer_name:
        resource = ckan_model.Resource.get(resource_id)

    geoserver = Geoserver.from_ckan_config()

    package_id = ckan_model.Resource.get(resource_id).resource_group.package_id

    def unpub():
        if geoserver_layer_name is not None:
            layer = Layer(geoserver=geoserver, layer_name=geoserver_layer_name, resource_id=resource_id,
                          package_id=package_id, username=username)
            return layer
        else:
            layer = Layer(geoserver=geoserver, layer_name=layer_name, resource_id=resource_id,
                          package_id=package_id,
                          username=username)
            return layer

    try:
        layer = unpub()
    except socket.error:
        h.flash_error(
            _("Error connecting to geoserver. Please contact the site administrator if this problem persists."))
        return False

    layer.remove()
    h.flash_success(
        _("This resource has successfully been unpublished."))
    return True


def get_wms_for_pkg(context, data_dict):
    """
    This method takes in a data_dict that contains a key called pkg_id whose value is the id of a ckan package
    and constructs WMS URLs from WMS resources contained in the package and returns the URLs to the caller.
    """
    pkg_id = data_dict.get("pkg_id")
    pkg = toolkit.get_action("package_show")(None, {'id': pkg_id})

    def is_wms_resource(resource):
        if 'protocol' in resource and resource.get('protocol').lower() == 'ogc:wms':
            return True
        return False

    wms_resources = filter(is_wms_resource, pkg.get('resources'))

    def construct_wms_url(resource):
        url = resource.get('url').split('?')[0]
        layer_name = ''
        try:
            wms = WebMapService(url, '1.1.1')
            layers = list(wms.contents)
            first_layer = layers[0]

            if 'layer_name' in resource:
                if resource.get('layer_name').lower() in layers:
                    layer_name = resource.get('layer_name').lower()

            if layer_name == '':
                layer_name = first_layer

        except Exception:
            pass

        return {
            'layer': layer_name,
            'url': url
        }


    wms_urls = map(construct_wms_url, wms_resources)
    return wms_urls

#def GETLayerNameWMS(context, data_dict):
#    resource_id = data_dict.get("resource_id")
#    file_resource = toolkit.get_action("resource_show")(None, {"id": resource_id})
#    thisData = file_resource
#    thisURL = thisData.get("url")
#    thisWMS = WebMapService(thisURL, "1.1.1")
#
#    def get_layer_list():
#        return list(thisWMS.contents)
#
#    def get_first_layer():
#        theseLayers = get_layer_list()
#        return theseLayers[0]
#
#    layers = list(thisWMS.contents)
#
#    given_layer = thisData.get("layer_name")
#    if not given_layer:
#        thisData.get("layer")
#    if not given_layer:
#        thisData.get("layers")
#
#    if given_layer in layers:
#        return given_layer
#    else:
#        return get_first_layer()
