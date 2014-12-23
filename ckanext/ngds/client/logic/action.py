from ckanext.ngds.common import plugins as p
from ckanext.ngds.common import logic
from ckanext.ngds.client.model import ogc

import urllib
from pylons import config
from urlparse import urlparse

def geothermal_prospector_url(context, data_dict):
    try:
        search = logic.action.get.resource_show(context, data_dict)
        gtp_url = 'https://maps-stage.nrel.gov/geothermal-prospector/#/'
        gtp_layer = '6'
        wms = ogc.HandleWMS(search['url'])
        wms_info = wms.get_layer_info(search)
	service_url = wms_info['service_url']

	#PROXY SETTING
        #If geoserver is under proxy, change service_url to proxied one in order to show wms layer by JS
        useProxy = config.get("geoserver.use_proxy", False)
        ProxiedPath = config.get("geoserver.proxied_path", None)
        siteUrl = config.get("ckan.site_url", "http://127.0.0.1")

        if useProxy and ProxiedPath and siteUrl:
            urlParsed = urlparse(service_url)
            #Generate proxied geoserver link (path.replace: it replaces original goeserver path with proxied path)
            service_url = siteUrl+urlParsed.path.replace('/geoserver', ProxiedPath)+'?'+urlParsed.query

        #END PROXY SETTING

        url = gtp_url + '?baselayer=' + gtp_layer + '&zoomlevel=3&wmsHost=' \
              + urllib.quote(service_url, '') + '&wmsLayerName=' \
              + wms_info['layer']
        return url
    except:
        return 'error'
