from ckan.lib.base import model,h,g,c,request
import ckanext.ngds.geoserver.logic.action as geoserver_actions
import ckan.logic as logic
NotFound = logic.NotFound
from pylons import config

def is_spatialized(res_id,col_geo):
	context = {'model': model, 'session': model.Session,\
                   'user': c.user or c.author, 'for_view': True}
	try:
		is_spatialized = geoserver_actions.datastore_is_exposed_as_layer(context,{'id':res_id})['is_exposed_as_layer']
		print is_spatialized
	except(NotFound):
		is_spatialized = False
	return is_spatialized