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

        # use url_ogc if wms is hosted on the local geoserver
        wms_url_type  = 'url_ogc' if 'url_ogc' in search  else 'url' 
        gtp_url       = 'https://maps-stage.nrel.gov/geothermal-prospector/#/'
        gtp_layer     = '6'
        wms           = ogc.HandleWMS(search[wms_url_type])
        wms_info      = wms.get_layer_info(search)
	service_url   = wms_info['service_url']

        url = gtp_url + '?baselayer=' + gtp_layer + '&zoomlevel=3&wmsHost=' \
              + urllib.quote(service_url, '') + '&wmsLayerName=' \
              + wms_info['layer']
    except:
	return 'error'

    #Incase Exception, return URL because Geothermal Propector doesn't require WFS Parameters to be set
    try:
	#get WFS related by parent_resource's WMS distribution
	results       = get_action('resource_search')(context, {'query': 'parent_resource:'+search.get('parent_resource', None)})
	count         = results.get('count', None)
	aWFSResources = results.get('results', [])
	
	if count :
	    #loop in resources until we find WFS

	    for WFSResource in aWFSResources:

                # use url_ogc if wfs is hosted on the local geoserver
                wfs_url_type = 'url_ogc' if WFSResource.get('url_ogc', None) else 'url'

		if WFSResource.get('protocol', None) == 'OGC:WFS' and WFSResource.get(wfs_url_type, None):
		    wfs         = ogc.HandleWFS(WFSResource.get(wfs_url_type, None))
		    wfs_feature = wfs.do_layer_check({'resource': WFSResource})
        	    service_url = wfs.get_service_url()
		    url         = url + '&wfsHost=' + urllib.quote(service_url, '') + '&wfsFeatureTypeName=' + wfs_feature

	            break
    except:
        return url

    return url
