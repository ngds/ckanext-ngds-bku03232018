from ckanext.ngds.common import plugins as p
from ckanext.mapsearch.common import logic
from ckanext.ngds.client.model import ogc

def geothermal_prospector_url(context, data_dict):
    try:
        search = logic.action.get.resource_show(context, data_dict)
        gtp_url = 'https://maps-stage.nrel.gov/geothermal-prospector/#/'
        gtp_layer = '6'
        wms = ogc.HandleWMS(search['url'])
        wms_info = wms.get_layer_info({})
        url = gtp_url + '?baselayer=' + gtp_layer + '&zoomlevel=3&wmsHost=' \
              + wms_info['service_url'].replace('?', '') + '&wmsLayerName=' \
              + wms_info['layer']
        return url
    except:
        return 'error'
