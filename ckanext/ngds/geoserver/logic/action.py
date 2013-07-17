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

    # Check that you have everything you need
    if None in [resource_id, layer_name, username, package_id]:
        raise Exception("Not enough information to publish resource")

    # Publish a layer
    l = Layer.publish(package_id, resource_id, layer_name, username, lat_field=lat_field, lng_field=lng_field)

    # Confirm that everything went according to plan
    if l is None:
        raise Exception("Layer generation failed")
    else:
        # csv content should be spatialized or a shapefile uploaded, Geoserver updated, resources appended.
        #  l should be a Layer instance. Return whatever you wish to
        return "Success"

'''
def publish(context, data_dict):
    """
    Create a spatialized dataset and expose it to Geoserver
    """
    package_id = data_dict.get("package_id")
    resource_id = data_dict.get("resource_id")
    latitude_field = data_dict.get("col_latitude")
    longitude_field = data_dict.get("col_longitude")
    username = context['user']

    resource = toolkit.get_action('resource_show')(context, {'id': resource_id})

    format = resource.get('format')

    if format and format.lower() == 'csv':
        # CSV files are already ingested via Datastorer
        data_stored = Datastored(resource_id, latitude_field, longitude_field)

        # Spatialize the table
        data_stored.publish()

        # Specify the name of the layer
        layer_name = resource_id
    elif format and format.lower() == 'zip':
        # Access the resource's shapefile
        sf = Shapefile(resource_id)

        # Find output location and name
        output_location = sf.get_destination_source()
        name = sf.get_source_layer().GetName()

        # Generate the destination PostGIS table (the destination_layer starts empty)
        if sf.create_destination_layer(output_location, name):
            layer_name = name
            output_layer = sf.get_destination_layer(output_location, name)

            # Push the shapefile into the PostGIS table
            sf.publish(output_layer)
    else:
        raise Exception("Can't spatialize files other than .csv and .zip.")

    # Add the content to Geoserver
    return Layer(
        geoserver=Geoserver.from_ckan_config(),
        layer_name=layer_name,
        resource_id=resource_id,
        package_id=package_id,
        username=username
    ).create()
'''

def unpublish(context,data_dict):
    """

    """
    resource_id = data_dict.get("resource_id")
    # layer_name = data_dict.get("layer_name")
    layer_name = "NGDS:"+resource_id
    username =  context.get('user')
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

    layer = Layer(geoserver=geoserver, layer_name=layer_name, resource_id=resource_id,package_id=package_id,username=username)
    print "next here"
    layer.remove()
    print "finished"
    return True
