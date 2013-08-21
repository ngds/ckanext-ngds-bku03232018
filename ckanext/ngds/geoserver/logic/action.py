import logging
import ckan.logic as logic
from ckanext.ngds.geoserver.model.Geoserver import Geoserver
from ckanext.ngds.geoserver.model.Datastored import Datastored
from ckanext.ngds.geoserver.model.ShapeFile import Shapefile
from ckanext.ngds.geoserver.model.Layer import Layer
from ckan.plugins import toolkit
from ckanext.ngds.env import ckan_model

from geoserver.catalog import Catalog

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
    # Gather inputs
    resource_id = data_dict.get("resource_id", None)
    layer_name = data_dict.get("layer_name", resource_id)
    username = context.get("user", None)
    package_id = data_dict.get("package_id", None)
    lat_field = data_dict.get("col_latitude", None)
    lng_field = data_dict.get("col_longitude", None)
    file_resource = toolkit.get_action("resource_show")(None, {"id": resource_id})
    geoserver_layer_name = file_resource.get("geoserver_layer_name")

    # Check that you have everything you need
    if None in [resource_id, layer_name, username, package_id]:
        raise Exception("Not enough information to publish resource")

    # Publish a layer
    def pub():
        if geoserver_layer_name is not None:
            l = Layer.publish(package_id, resource_id, layer_name, username, lat_field=lat_field, lng_field=lng_field)
            return l
        else:
            l = Layer.publish(package_id, resource_id, layer_name, username, lat_field=lat_field, lng_field=lng_field)
            return l

    l = pub()

    # Confirm that everything went according to plan
    if l is None:
        raise Exception("Layer generation failed")
    else:
        # csv content should be spatialized or a shapefile uploaded, Geoserver updated, resources appended.
        #  l should be a Layer instance. Return whatever you wish to
        return "Success"

def unpublish(context,data_dict):
    """

    """
    resource_id = data_dict.get("resource_id")
    # layer_name = data_dict.get("layer_name")
    layer_name = "NGDS:"+resource_id
    username =  context.get('user')
    file_resource = toolkit.get_action("resource_show")(None, {"id": resource_id})
    geoserver_layer_name = file_resource.get("geoserver_layer_name")

    if not layer_name:
        resource = ckan_model.Resource.get(resource_id)
        # layer_name = resource.get('layer_name')

    geoserver = Geoserver.from_ckan_config()

    package_id = ckan_model.Resource.get(resource_id).resource_group.package_id
    print "here"
    # package = ckan_model.Package.get(package_id)

    # for resource in package.resources:
    #     if 'parent_resource' in resource.extras and 'ogc_type' in resource.extras:
    #         extras = resource.extras
    #         if extras['parent_resource'] == resource_id:
    #             layer_name = extras['layer_name']
    #             break
    def unpub():
        if geoserver_layer_name is not None:
            layer = Layer(geoserver=geoserver, layer_name=geoserver_layer_name, resource_id=resource_id,package_id=package_id,username=username)
            return layer
        else:
            layer = Layer(geoserver=geoserver, layer_name=layer_name, resource_id=resource_id,package_id=package_id,username=username)
            return layer

    layer = unpub()

    print "next here"
    layer.remove()
    print "finished"
    return True
