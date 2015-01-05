from ckanext.ngds.common import plugins as p
from ckanext.ngds.common import logic
from ckanext.ngds.client.model import ogc

import urllib
from pylons import config
from urlparse import urlparse

get_action = logic.get_action

def geothermal_prospector_url(context, data_dict):
    try:
        search = logic.action.get.resource_show(context, data_dict)
        gtp_url = 'https://maps-stage.nrel.gov/geothermal-prospector/#/'
        gtp_layer = '6'
        wms = ogc.HandleWMS(search['url'])
        wms_info = wms.get_layer_info(search)
	service_url = wms_info['service_url']

        url = gtp_url + '?baselayer=' + gtp_layer + '&zoomlevel=3&wmsHost=' \
              + urllib.quote(service_url, '') + '&wmsLayerName=' \
              + wms_info['layer']
    except:
	return 'error'

    #Incase Exception, return URL because Geothermal Propector doesn't require WFS Parameters to be set
    try:
	#get WFS related by parent_resource's WMS distribution
	results = get_action('resource_search')(context, {'query': 'parent_resource:'+search.get('parent_resource', None)})
	count = results.get('count', None)
	aWFSResources = results.get('results', [])
	
	if count :
	    #loop in resources until we find WFS
	    for WFSResource in aWFSResources:
		if WFSResource.get('protocol', None) == 'OGC:WFS' and WFSResource.get('url', None):
		    wfs = ogc.HandleWFS(WFSResource.get('url', None))
		    wfs_feature = wfs.do_layer_check({'resource': WFSResource})
        	    service_url = wfs.get_service_url()

		    url = url + '&wfsHost=' + urllib.quote(service_url, '') + '&wfsFeatureTypeName=' + wfs_feature

	            break
    except:
        return url

    return url
