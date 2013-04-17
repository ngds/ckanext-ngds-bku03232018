from ckan.lib.base import model,h,g,c,request
import ckan.lib.navl.dictization_functions as dictization_functions
import ckanext.ngds.geoserver.logic.action as geoserver_actions
DataError = dictization_functions.DataError
from pylons import config


def get_responsible_party_name(id):
	"""
	Get the name of a responsible party for an id.
	"""
	# If we don't get an int id, return an empty string.
	if id:
		try:
			id_int = int(id)
		except(ValueError):
			return ""
		responsible_party = model.ResponsibleParty.get(id)
		if responsible_party:
			return responsible_party.name
		else:
			return ""
	else:
		return ""

def get_login_url():
	x = request.url
	print x
	return h.url_for(_get_repoze_handler('login_handler_path'),came_from=x)

def _get_repoze_handler(handler_name):
    '''Returns the URL that repoze.who will respond to and perform a
    login or logout.'''
    return getattr(request.environ['repoze.who.plugins']['friendlyform'],handler_name)

def get_default_group():

	try:
		print g.default_group
	except AttributeError:
		g.default_group = config.get('ngds.default_group_name', 'public')

	return g.default_group

def get_language(id):
	if id:
		print "got id : "+id
		try:
			id_int = int(id)
		except(ValueError):
			return ""
		language = model.Language.get(id)
		print "Got language ",language
		print language.name
		if language:
			return language.name
		else:
			return ""
	else:
		return ""

def is_spatialized(res_id,col_geo):
	context = {'model': model, 'session': model.Session }
	return geoserver_actions.datastore_is_spatialized(context,{res_id,col_geo})
