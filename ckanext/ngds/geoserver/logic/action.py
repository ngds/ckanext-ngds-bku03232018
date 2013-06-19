import logging
import ckan.logic as logic
from ckanext.ngds.geoserver.model.Geoserver import Geoserver
from ckanext.ngds.geoserver.model.ShapeFile import Shapefile
from ckanext.ngds.geoserver.model.Layer import Layer
from ckan.plugins import toolkit

log = logging.getLogger(__name__)
_get_or_bust = logic.get_or_bust


def is_layer_exists(context,data_dict):
    """
    Checks whether layer exists in the geoserver. If not then returns False.

    @return:
    """
    is_exists = False

    return is_exists


def spatialize(context,data_dict):
    """

    """

    print "spatialize"

    return


def despatialize(context,data_dict):
    """

    """

    print "despatialize"

    return

def test(context,data_dict):
    resource_id = data_dict.get("resource_id")
    if resource_id:
        sf = Shapefile(resource_id)
        #sf.default_publish()

        output_location = sf.get_destination_source()
        if sf.create_destination_layer(output_location, sf.get_source_layer().GetName()):
            output_layer = sf.get_destination_layer(output_location, sf.get_source_layer().GetName())
            sf.publish(output_layer)
            return True

    return False
