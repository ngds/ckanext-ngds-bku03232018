from ckanext.ngds.common import plugins as p
from ckanext.ngds.client.model import ogc

def geothermal_prospector_url(context, data_dict):
    try:
        res_url = data_dict['url']
        gtp_url = 'https://maps-stage.nrel.gov/geothermal-prospector/#/'
        gtp_layer = '6'
        wms = ogc.HandleWMS(res_url)
        wms_info = wms.get_layer_info({})
        return {'wms': gtp_url + '?baselayer=' + wms_info + '&zoomlevel=3'}
    except:
        return {'wms': 'undefined'}
