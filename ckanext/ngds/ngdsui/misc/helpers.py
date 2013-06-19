from ckan.lib.base import model,h,g,c,request,response
import ckan.lib.navl.dictization_functions as dictization_functions
import ckan.logic as logic
import ckan.controllers.storage as storage
from ckan.model import User
DataError = dictization_functions.DataError
from pylons import config, jsonify
from datetime import date
import iso8601
import inspect
import re
from ckan.model.resource import Resource

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

def file_path_from_url(url):
    """
    Given a file's URL, find the file itself on this system

    @param url: The URL for a file that lives on this server
    @return: the file path to the file itself
    """

    pattern = "^(?P<protocol>.+?)://(?P<host>.+?)/.+/(?P<label>\d{4}-.+)$"
    label = re.match(pattern, url).group("label")
    return get_url_for_file(label)

def get_url_for_file(label):
    bucket = config.get('ckan.storage.bucket', 'default')
    ofs = storage.get_ofs()
    return ofs.get_url(bucket, label).replace("file://", "")

def is_plugin_enabled(plugin):
    plugins = config.get('ckan.plugins').split(' ')
    if plugin in plugins:
        return True
    return False

def username_for_id(id):
    return model.User.get(id).name

def get_formatted_date(timestamp):
    return iso8601.parse_date(timestamp).strftime("%B %d,%Y")

'''
This method loads the ngds facet configuration file and finds the facets to be during the search.

    **Parameters:**
    None.

    **Results:**
    :returns: The facets dict to be used for search.
    :rtype: OrderedDict    
'''

def load_ngds_facets():

    # Return the loaded facets from global context if available. This will avoid unnecssary reading of config file everytime during search.
    try:
        if g.loaded_facets:
            return g.loaded_facets
    except AttributeError:
        print "facets are yet to be loaded from the config."


    # Read the facet config file path from application config file (developement.ini)
    facets_config_path = config.get('ngds.facets_config')


    if facets_config_path:
        loaded_facets = read_facets_json(facets_config_path=facets_config_path)

    # If facets are loaded and available then set them in global context and return.
    if loaded_facets:
        g.loaded_facets = loaded_facets
        facets_dict = loaded_facets

    return  facets_dict


'''
This Method loads the given facets config file and constructs the facets structure to be used.
    **Parameters:**
    facets_config_path - Facets Configuration file (json file) path.

    **Results:**
    :returns: The facets dict to be used for search.
    :rtype: OrderedDict    
'''
def read_facets_json(facets_config_path=None):

    #Open the json config file and load it as dict.
    with open(facets_config_path, 'r') as json_file:
        import json
        from pprint import pprint
        json_data = json.load(json_file)

        #Dict structure of json config file is placed on global context for future use.
        g.facet_json_data = json_data

        facets_list = []
        #Pass each facet to read_facet method to find the list of fields.
        for facet in json_data:
            facets_list = read_facet(facet,facets_list)

    if facets_list:
        return OrderedDict(facets_list)
    else:
        return None

'''
Reads the input facet_config and its subfacets to find the metadatafields which will be used to used as facets. 
    **Parameters:**
    facet_struc - Particular facet structure to be iterated.
    facets_list - list of found facets to which new facets needs to be added into.

    **Results:**
    :returns: The facets list 
    :rtype: list
'''
def read_facet(facet_struc,facet_list):

    #If the metadatafield exists in the facet then add it to the list.
    if facet_struc.get("metadatafield") :
        facet_list.append((facet_struc['metadatafield'],_(facet_struc.get("facet") or facet_struc.get("display_name"))))

    #If subfacet exists then iterate through entire structure to find the remaining facets.
    if facet_struc.get("subfacet"):
        for subfacet in facet_struc.get("subfacet"):
            facet_list = read_facet(subfacet,facet_list)

    return facet_list

'''
This method gets the facets from search results and construct them into NGDS specific structure based on the facet json config file.

    **Parameters:**
    None.

    **Results:**
    :returns: Faceted results dict found from the results.
    :rtype: Dict    
'''
def get_ngdsfacets():

    facet_config = g.facet_json_data

    facets = []
    for facet_group in facet_config:
        facet_dict = {}
        facets.append(construct_facet(facet_group,facet_dict=facet_dict,facet_level=1))

    return facets

'''
This method constructs the facet results for each Facet structure (from json file) 

    **Parameters:**
    facet_group - Facet Structure to be filled based on results.
    facet_dict - newly constrcuted facets dict which needs to be appended with new values.
    metadatafield - Metadata field of the facet.
    facet_level - 1 - Top level facet 2 - Other sub level facets.
    facet_values - Values of the facets returned from search.


    **Results:**
    :returns: Constructed faceted dict from the input facet structure and the results.
    :rtype: Dict    
'''
def construct_facet(facet_group,facet_dict={},metadatafield=None,facet_level=1,facet_values=None):


    #If metadatafield exists, then get the faceted values from the search results.
    if facet_group.get("metadatafield") :
        metadatafield = facet_group['metadatafield']
        facet_dict['facet_field'] = metadatafield
        facet_values = h.get_facet_items_dict(metadatafield)


    facet_type = facet_group.get("type")

    facet_dict['type'] = facet_type


    # Display type of the field is determined here. If the facet level is 1 (i.e. called from get_ngdsfacets()) then it shld be top level title.
    #Otherwise it will be sub-title. In some cases, top level facet itself will be of type dynamic_keywords. Those types shld be displayed as titles.
    if facet_type == "title" or (facet_type == "dynamic_keywords" and not facet_group.get("subfacet")):
        if facet_level == 1:
            display_type = "title"
        else:
            display_type = "subtitle"
    else:
        display_type = "facet"

    #If the displaye_name exits then display that otherwise display facet itself.
    facet_dict['display_name'] = facet_group.get('display_name') or facet_group.get('facet')
    facet_dict['display_type'] = display_type

    #if the facet_type is dynamic_keywords then there won't be any sub-facets. Display those dynamic facet values .
    if facet_group.get("type") == 'dynamic_keywords':
        facet_dict['fvalues'] = facet_values

    #If the facet_type is "keyword" then it has to be compared with the results for the count. If matches then remove that from the results so that it won't be in the others list.
    #If the facet is not matching with any results, then create a dummy facet with count 0.
    if facet_group.get("type") == 'keyword':
        found = False
        for ret_facet in facet_values:
            #print "ret_facet['name']: ",ret_facet['name']
            if ret_facet['name'] == facet_group.get('facet'):
                if facet_group.get('display_name'):
                    ret_facet['display_name'] = facet_group['display_name']
                facet_dict['fvalues'] = [ret_facet]
                found = True
                facet_values.remove(ret_facet)
                break

        if not found:
            active = False
            if display_type == "facet":
                if (facet_dict['facet_field'], facet_group.get('facet')) in request.params.items():
                    active = True
            facet_dict['fvalues'] = [ {'count': 0,'active': active,'display_name': facet_dict.get('display_name'),'name': facet_group.get('facet')}]

    #If subfacet exists in the facet then iterate through the entire sub-facet structure to construct the results.
    if facet_group.get("subfacet"):
        subfacet_dict = []
        for subfacet in facet_group.get("subfacet"):
            subfacet_dict.append(construct_facet(subfacet,facet_dict={"facet_field":metadatafield},metadatafield=metadatafield,facet_level=2,facet_values=facet_values))
        facet_dict['subfacet'] = subfacet_dict

    return facet_dict

def get_formatted_date(datstr):
    from datetime import datetime
    return datetime.strptime(datstr[:10], '%Y-%m-%d').strftime('%b %d,%Y')

def to_json(data):
    #print json.dumps(data)
    return json.dumps(data)

def is_string_field(field_name):
    non_string_fields = ('publication_date')

    if field_name in non_string_fields:
        return False;

    return True;

def get_field_title(field_name):
    field_dict={'publication_date':'Publication Date','metadata_created':'Created Date'}

    print "Field Name:",field_name

    x = field_dict.get(field_name)

    print "Title:", x

    return x

def is_ogc_publishable(resource_id):
    resource = Resource.get(resource_id)
    url = resource.url
    if url[len(url)-3:len(url)]=='zip' or url[len(url)-3:len(url)]=='csv':
        return True
    return False

@jsonify
def jsonify(input):
    # Trivial as this may seem, it is neccessary.
    response.headers['Content-Type'] = 'text/html;charset=utf-8'
    return input