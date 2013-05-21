from ckan.lib.base import model,h,g,c,request
import ckan.lib.navl.dictization_functions as dictization_functions
import ckan.logic as logic
import ckan.controllers.storage as storage
DataError = dictization_functions.DataError
from pylons import config
import inspect

import ckan.plugins as p
_ = p.toolkit._

try:
    from collections import OrderedDict # 2.7
except ImportError:
    from sqlalchemy.util import OrderedDict

def get_responsible_party_name(id):
	"""
	Get the name of a responsible party for an id.
	"""
	print "get_responsible_party_name  " 
	print id
	#print inspect.stack()
	# frm = inspect.stack()[0]
	# mod = inspect.getmodule(frm[0])
	# print '[%s] %s' % (mod.__name__, id)
	# If we don't get an int id, return an empty string.
	if id  and isinstance(id,basestring)==True:
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

def get_url_for_file(label):
	# storage_controller = StorageController()
	BUCKET = config.get('ckan.storage.bucket', 'default')
	ofs = storage.get_ofs()
	print ofs.get_url(BUCKET,label)
	return ofs.get_url(BUCKET,label)

def is_plugin_enabled(plugin):
	plugins = config.get('ckan.plugins').split(' ')
	if plugin in plugins:
		return True
	return False

def load_ngds_facets():
    try:
        if g.loaded_facets:
            return g.loaded_facets
    except AttributeError:
        print "facets are yet to be loaded from the config."

    facets_config_path = config.get('ngds.facets_config')


    if facets_config_path:
        loaded_facets = read_facets_json(facets_config_path=facets_config_path)
    
    if loaded_facets:
        g.loaded_facets = loaded_facets
        facets_dict = loaded_facets

    return  facets_dict

def read_facets_json(facets_config_path=None):
    '''
    This Method loads the given facets config file and constructs the facets structure to be used.
    '''

    with open(facets_config_path, 'r') as json_file:
        import json
        from pprint import pprint
        json_data = json.load(json_file)

        g.facet_json_data = json_data

        #facets_dict =OrderedDict()
        facets_list = []

        for facet in json_data:
            facets_list = read_facet(facet,facets_list)

    if facets_list:
        return OrderedDict(facets_list)
    else:
        return None

def read_facet(facet_config,facet_list):

    if facet_config.get("metadatafield") :
        facet_list.append((facet_config['metadatafield'],_(facet_config.get("facet"))))

    if facet_config.get("subfacet"):
        for subfacet in facet_config.get("subfacet"):
            facet_list = read_facet(subfacet,facet_list)

    return facet_list


def get_ngdsfacets():
    print "entering facets..."
    facet_config = g.facet_json_data

    facets = []

    for facet_group in facet_config:
        facet_dict = {}
        facets.append(construct_facet(facet_group,facet_dict=facet_dict,facet_level=1))
    import json
    print "Constructed Facets: ",json.dumps(facets)

    return facets

def construct_facet(facet_group,facet_dict={},metadatafield=None,facet_level=1,facet_values=None):

    #print "facet_group: ",facet_group
    print "facet_group.get(metadatafield):",facet_group.get("metadatafield")

    if facet_group.get("metadatafield") :
        metadatafield = facet_group['metadatafield']
        facet_dict['facet_field'] = metadatafield
        facet_values = h.get_facet_items_dict(metadatafield)
        #print "facet_values:",facet_values

    facet_dict['type'] = facet_group.get("type")
    if facet_group.get("type") == "title":
        if facet_level == 1:
            facet_type = "title"
        else:
            facet_type = "subtitle"
    else:
        facet_type = "facet"

    facet_dict['display_name'] = facet_group.get('display_name') or facet_group.get('facet')
    facet_dict['display_type'] = facet_type

    '''
    [{'count': 1, 'active': False, 'display_name': u'wells', 'name': u'wells'}, {'count': 1, 'active': False, 'display_name': u'Geology', 'name': u'Geology'}]
    '''

    if facet_group.get("type") == 'dynamic_keywords':
        facet_dict['fvalues'] = facet_values

    if facet_group.get("type") == 'keyword':
        found = False
        for ret_facet in facet_values:
            if ret_facet['name'] == facet_group.get('facet'):
                if facet_group.get('display_name'):
                    ret_facet['display_name'] = facet_group['display_name']
                facet_dict['fvalues'] = [ret_facet]
                found = True
                facet_values.remove(ret_facet)
                break
        if not found:
            facet_dict['fvalues'] = [ {'count': 0,'active': False,'display_name': facet_dict.get('display_name'),'name': facet_group.get('facet')}]

    if facet_group.get("subfacet"):
        subfacet_dict = []
        for subfacet in facet_group.get("subfacet"):
            subfacet_dict.append(construct_facet(subfacet,facet_dict={"facet_field":metadatafield},metadatafield=metadatafield,facet_level=2,facet_values=facet_values))
        facet_dict['subfacet'] = subfacet_dict

    return facet_dict