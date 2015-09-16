from ckanext.ngds.common import plugins as p
from ckanext.ngds.common import logic
from ckanext.ngds.client.model import ogc

import urllib
import ckan.model as model
from pylons import config
from urlparse import urlparse

get_action = logic.get_action

import pprint
pp = pprint.PrettyPrinter(indent=4)


def geothermal_prospector_url(context, data_dict):

    try:
        search     = logic.action.get.resource_show(context, data_dict)
        package_id = _get_package_id(search['id'])

        # use url_ogc if wms is hosted on the local geoserver
        wms_url_type  = 'url_ogc' if 'url_ogc' in search  else 'url' 
        gtp_url       = 'https://maps.nrel.gov/geothermal-prospector/#/'
        gtp_layer     = '6'
        wms           = ogc.HandleWMS(search[wms_url_type])
        wms_info      = wms.get_layer_info(search)
	service_url   = wms_info['service_url']
        resource_gid  = search['resource_group_id']

        url = gtp_url + '?baselayer=' + gtp_layer + '&zoomlevel=3&wmsHost=' \
              + urllib.quote(service_url, '') + '&wmsLayerName=' \
              + wms_info['layer']
    except:
	return 'error'

    #Incase Exception, return URL because Geothermal Propector doesn't require WFS Parameters to be set
    try:
	#get WFS
	results       = get_action('package_show')(context, {'id': package_id})
	count         = results.get('num_resources', None)
	aWFSResources = results.get('resources', [])

	if count :
	    #loop in resources until we find WFS

	    for WFSResource in aWFSResources:

                wfs_formats = ['wfs', 'ogc:wfs']
                wfs_format  = WFSResource.get('format', None)

		if WFSResource.get(wms_url_type, None) and wfs_format in wfs_formats:

		    wfs         = ogc.HandleWFS(WFSResource.get(wms_url_type, None))
		    wfs_feature = wfs.do_layer_check({'resource': WFSResource})
        	    service_url = wfs.get_service_url()
                    url         = url + '&wfsHost=' + urllib.quote(service_url, '') + '&wfsFeatureTypeName=' + wfs_feature

	            break
    except:
        return url

    return url

def _get_package_id(resource_id):

    sql = '''SELECT resource_group.package_id as package_id
             FROM resource, resource_group
             WHERE resource.id='%s' AND resource.resource_group_id=resource_group.id''' % resource_id
    try:
        package_id = model.Session.execute(sql).fetchone().package_id
    except:
        return 'error'

    return package_id
