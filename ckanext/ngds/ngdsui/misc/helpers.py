"""
This file defines a list of helper functions that are used from the site templates to obtain data that may not be available at the time of rendering, or to process information on the fly.
"""
from ckan.lib.base import model, h, g, c, request, response
import ckan.lib.navl.dictization_functions as dictization_functions
import ckan.controllers.storage as storage
from webhelpers.html import literal
import ckan.rating as rating

DataError = dictization_functions.DataError
from pylons import config, jsonify
import ckan.logic as logic

from ckanext.ngds.env import ckan_model

import iso8601
import urllib2

import re
from ckan.model.resource import Resource
import logging
import ckan.plugins as p
import json

from ckan.plugins import toolkit

try:
    from collections import OrderedDict # 2.7
except ImportError:
    from sqlalchemy.util import OrderedDict

log = logging.getLogger(__name__)


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
    if id and isinstance(id, basestring) == True:
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
    return h.url_for(_get_repoze_handler('login_handler_path'), came_from=x)


def _get_repoze_handler(handler_name):
    '''Returns the URL that repoze.who will respond to and perform a
    login or logout.'''
    return getattr(request.environ['repoze.who.plugins']['friendlyform'], handler_name)


def get_default_group():
    """
    Returns the default group name that is configured in the site configuration file.
    """
    default_group_id = ''
    try:
        default_group_id = g.default_group
    except Exception:
        default_group_id = config.get('ngds.default_group_name', 'public')

    return default_group_id


def highlight_rating_star(count, packageId):
    """
    Accepts a rating value and returns a 1 to indicate that a star must be highlighted on the UI to indicate a rating, and a 0 to not highlight it.
    """
    package = model.Package.get(packageId)
    if rating.get_rating(package)[0] >= count:
        return 1
    else:
        return 0


def get_rating_details(package_id):
    """
    Returns the average rating of a package for a given package id and the number of ratings.
    """
    rating_obj = rating.get_rating(model.Package.get(package_id))
    rating_v = rating_obj[0] or 0
    ratings_count = rating_obj[1]
    rnd = round(rating_v)
    intv = int(rnd)
    return intv, ratings_count


def count_rating_reviews(packageId):
    package = model.Package.get(packageId)
    if (rating.get_rating(package)):
        return rating.get_rating(package)[1]
    else:
        return 0


def rating_text(count):
    """
    Returns the text to be displayed for a given rating value
    """
    if count == 1:
        return toolkit._("Rate as very poor?")
    else:
        if count == 2:
            return toolkit._("Rate as poor?")
        else:
            if count == 3:
                return toolkit._("Rate as fair?")
            else:
                if count == 4:
                    return toolkit._("Rate as good?")
                else:
                    return toolkit._("Rate as very good?")


def get_language(id):
    """
    Returns the language name for a given language id.
    """
    if id:
        try:
            id_int = int(id)
        except(ValueError):
            return ""
        language = model.Language.get(id)
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
    return get_url_for_file(urllib2.unquote(label))


def get_url_for_file(label):
    """
    Returns the URL for a file given it's label.
    :return:
    """
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


def get_formatted_date_from_obj(timestamp, isdate):
    if isdate:
        return timestamp.strftime("%b %d, %Y %H:%M")
    else:
        return iso8601.parse_date(timestamp).strftime("%b %d,%Y %H:%M")


def load_ngds_facets():
    """
    This method loads the ngds facet configuration file and finds the facets to be during the search.

        **Parameters:**
        None.

        **Results:**
        :returns: The facets dict to be used for search.
        :rtype: OrderedDict
    """

    # Return the loaded facets from global context if available. This will avoid unnecssary reading of config file everytime during search.
    try:
        if g.loaded_facets:
            return g.loaded_facets
    except AttributeError:
        log.info("facets are yet to be loaded from the config.")


    # Read the facet config file path from application config file (developement.ini)
    facets_config_path = config.get('ngds.facets_config')

    if facets_config_path:
        loaded_facets = read_facets_json(facets_config_path=facets_config_path)

    # If facets are loaded and available then set them in global context and return.
    if loaded_facets:
        g.loaded_facets = loaded_facets
        facets_dict = loaded_facets

    return facets_dict


def read_facets_json(facets_config_path=None):
    """
    This Method loads the given facets config file and constructs the facets structure to be used.
        **Parameters:**
        facets_config_path - Facets Configuration file (json file) path.

        **Results:**
        :returns: The facets dict to be used for search.
        :rtype: OrderedDict
    """
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
            facets_list = read_facet(facet, facets_list)

    if facets_list:
        return OrderedDict(facets_list)
    else:
        return None


def read_facet(facet_struc, facet_list):
    """
    Reads the input facet_config and its subfacets to find the metadatafields which will be used to used as facets.
        **Parameters:**
        facet_struc - Particular facet structure to be iterated.
        facets_list - list of found facets to which new facets needs to be added into.

        **Results:**
        :returns: The facets list
        :rtype: list
    """

    #If the metadatafield exists in the facet then add it to the list.
    if facet_struc.get("metadatafield"):
        facet_list.append(
            (facet_struc['metadatafield'], toolkit._(facet_struc.get("facet") or facet_struc.get("display_name"))))

    #If subfacet exists then iterate through entire structure to find the remaining facets.
    if facet_struc.get("subfacet"):
        for subfacet in facet_struc.get("subfacet"):
            facet_list = read_facet(subfacet, facet_list)

    return facet_list


def get_ngdsfacets():
    """
    This method gets the facets from search results and construct them into NGDS specific structure based on the facet json config file.

        **Parameters:**
        None.

        **Results:**
        :returns: Faceted results dict found from the results.
        :rtype: Dict
    """

    facet_config = g.facet_json_data

    facets = []
    for facet_group in facet_config:
        facet_dict = {}
        facets.append(construct_facet(facet_group, facet_dict=facet_dict, facet_level=1))

    return facets


def construct_facet(facet_group, facet_dict={}, metadatafield=None, facet_level=1, facet_values=None):
    """
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
    """

    #If metadatafield exists, then get the faceted values from the search results.
    if facet_group.get("metadatafield"):
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
            if str(ret_facet['name']).lower() == str(facet_group.get('facet')).lower():
                ret_facet['display_name'] = facet_group.get('display_name') or facet_group.get('facet')
                facet_dict['fvalues'] = [ret_facet]
                found = True
                facet_values.remove(ret_facet)
                break

        if not found:
            active = False
            if display_type == "facet":
                if (facet_dict['facet_field'], facet_group.get('facet')) in request.params.items():
                    active = True
            facet_dict['fvalues'] = [{'count': 0, 'active': active, 'display_name': facet_dict.get('display_name'),
                                      'name': facet_group.get('facet')}]

    #If subfacet exists in the facet then iterate through the entire sub-facet structure to construct the results.
    if facet_group.get("subfacet"):
        subfacet_dict = []
        for subfacet in facet_group.get("subfacet"):
            subfacet_dict.append(
                construct_facet(subfacet, facet_dict={"facet_field": metadatafield}, metadatafield=metadatafield,
                                facet_level=2, facet_values=facet_values))
        facet_dict['subfacet'] = subfacet_dict

    return facet_dict


def get_formatted_date(datstr):
    formated_string = ""
    if datstr:
        from datetime import datetime

        formated_string = datetime.strptime(datstr[:10], '%Y-%m-%d').strftime('%b %d,%Y')
    return formated_string


def to_json(data):
    #print json.dumps(data)
    return json.dumps(data)


def is_string_field(field_name):
    non_string_fields = ('publication_date')

    if field_name in non_string_fields:
        return False;

    return True;


def get_field_title(field_name):
    field_dict = {'publication_date': 'Publication Date', 'metadata_created': 'Created Date'}

    x = field_dict.get(field_name)

    return x


def is_ogc_publishable(resource_id):
    resource = Resource.get(resource_id)
    url = resource.url
    if url[len(url) - 3:len(url)] == 'zip' or url[len(url) - 3:len(url)] == 'csv':
        return True
    return False


@jsonify
def jsonify(input):
    # Trivial as this may seem, it is neccessary.
    response.headers['Content-Type'] = 'text/html;charset=utf-8'
    return input


def get_usersearches():
    user = model.User.by_name(c.user.decode('utf8'))
    query = model.UserSearch.search(user.id)

    return query.all()


def parseJSON(input):
    try:
        json_parsed = json.loads(input)
    except(ValueError, TypeError):
        return json.loads("{}")
    return json_parsed


def json_extract(input, key):
    if (input == ''):
        return ''
    try:
        input = input.decode('ascii').replace("&#34;", '"')
        i_json = json.loads(input)
        if key in i_json:
            print "Found : " + i_json[key] + " for key : " + key
            return i_json[key]
    except(ValueError):
        pass
    finally:
        return ''


def get_dataset_category_image_path(package):
    image_path = '/assets/dataset.png'

    dataset_category = None

    for extra in package.get('extras'):
        key = extra.get('key')
        if key and key == 'data_type':
            dataset_category = str(extra.get('value'))
            break

    category_image_link = {
        'Dataset': '/assets/dataset.png',
        'Physical Collection': '/assets/physicalcollection.png',
        'Catalog': '/assets/catalog.png',
        'Movie or Video': '/assets/video.png',
        'Drawing': '/assets/drawing.png',
        'Photograph': '/assets/photograph.png',
        'Remotely-Sensed Image': '/assets/remotelysensedimage.png',
        'Map': '/assets/map.png',
        'Text Document': '/assets/text_document.png',
        'Physical Artifact': '/assets/physicalcollection.png',
        'Desktop Application': '/assets/dataset.png',
        'Web Application': '/assets/dataset.png'
    }

    if dataset_category and dataset_category in category_image_link:
        image_path = category_image_link.get(dataset_category)

    return image_path


def is_following(obj_type, obj_id):
    '''Return a true/False based on follow for the given object type and id.

    If the user is not logged in return an empty string instead.

    :param obj_type: the type of the object to be followed when the follow
        button is clicked, e.g. 'user' or 'dataset'
    :type obj_type: string
    :param obj_id: the id of the object to be followed when the follow button
        is clicked
    :type obj_id: string

    :returns: a follow button as an HTML snippet
    :rtype: string

    '''
    obj_type = obj_type.lower()
    # If the user is logged in show the follow/unfollow button
    following = False
    if c.user:
        context = {'model': model, 'session': model.Session, 'user': c.user}
        action = 'am_following_%s' % obj_type
        # following = logic.get_action(action)(context, {'id': obj_id})
    return True


def create_package_resource_document_index(pkg_id, resource_dict_list):
    """
    Creates entry for the documents to be full-text indexed for a particular dataset or package. (resource_document_index table).
    Before creating new entries, existing to be indexed (status as 'NEW') entries are updated as 'CANCEL'.
    :returns: True after creating entries in db.
    """

    from ckanext.ngds.metadata.controllers.transaction_data import dispatch as trans_dispatch

    ckan_model.Session().execute(
        "UPDATE public.resource_document_index SET status=:status_val where package_id=:pkg_id and status=:old_status",
        {'status_val': 'CANCEL', 'pkg_id': pkg_id, 'old_status': 'NEW'})

    data_dict = {'model': 'DocumentIndex'}
    data_dict['process'] = 'add'
    context = {'model': ckan_model, 'session': ckan_model.Session}

    for index_dict in resource_dict_list:
        index_dict['status'] = 'NEW'
        data_dict['data'] = index_dict
        trans_dispatch(context, data_dict)

    return True


def get_docs_to_index(status):
    """
    Finds and returns all the documents to be indexed records from 'resource_document_index' table based on the input status.
    """

    query = ckan_model.DocumentIndex.search(status)

    return query.all()


def process_resource_docs_to_index():
    """
    This is the initial step to Full Text Indexing process. Will get all the documents to be indexed with status "NEW' and
    for each document's content will be extracted and updated to Dataset's solr indexing.
    """

    docs_to_index = get_docs_to_index('NEW')

    from ckanext.ngds.lib.index import FullTextIndexer

    text_indexer = FullTextIndexer()
    site_id = config.get('ckan.site_id', 'default')
    data_dict = {'site_id': site_id}
    for doc in docs_to_index:
        data_dict['id'] = doc.package_id
        field_to_add = 'resource_file_%s' % doc.resource_id
        text_indexer.index_resource_file(data_dict, field_to_add, doc.file_path, defer_commit=True)
        doc.status = 'DONE'
        doc.save()


def get_master_style():
    if config.get('ngds.is_development', "false") == "true":
        less_file = '<link rel="stylesheet/less" type="text/css" href="/css/main.less"/>'
        less_js = ' <script type="text/javascript" src="/vendor/less/less.min.js"></script>'
        return literal('%s %s' % (less_file, less_js))

    return literal('<link rel="stylesheet" type="text/css" href="/css/main.css"/>')


def split(what, how):
    return how.join(what)


def get_label_for_pkg_attribute(attribute):
    if attribute in label_attribute_mapping:
        return label_attribute_mapping[attribute]
    return attribute


def get_label_for_resource_attribute(attribute):
    s_attribute = str(attribute)
    print s_attribute
    if s_attribute in res_label_attribute_mapping:
        return res_label_attribute_mapping[s_attribute]
    return s_attribute


label_attribute_mapping = {
    u'data_type': u'Data Type',
    u'language': u'Language',
    u'lineage': u'Lineage',
    u'ngds_maintainer': u'Maintainers',
    u'publication_date': u'Publication Date',
    u'quality': u'Quality',
    u'spatial': u'Geographic Location',
    u'spatial_word': u'Geographic Location Tags',
    u'status': u'Status',
    u'uri': u'URI',
    u'authors': u'Authors'
}

res_label_attribute_mapping = {
    'dataset name': 'Dataset Name',
    'distributor': 'Distributor',
    'id': 'Id',
    'layer': 'Layer',
    'position': 'Position',
    'protocol': 'Protocol',
    'resource format': 'Resource Type',
    'resource group id': 'Resource Group Id',
    'revision id': 'Revision Id',
    'revision timestamp': 'Revision Timestamp',
    'state': 'State',
    'content model uri': 'Content Model URI',
    'format': 'Format',
    'geoserver layer name': 'Geoserver Layer',
    'geom extent': 'Geographic Extent',
    'layer name': 'Geoserver Layer Name',
    'parent resource': 'Parent Resource Id'
}


def is_json(value):
    try:
        json.loads(value)
        return True
    except(ValueError):
        pass
    return False


def is_development():
    if config.get('ngds.is_development', "false") == "true":
        return True
    return False


def get_top_5_harvest_sources():
    sources = logic.get_action('harvest_source_list')(None, {})
    top_sources = sorted(sources, key=lambda x: x['status']['overall_statistics']['added'])
    return top_sources[0:5]


def get_home_images():
    """
    Reads the home images configuration file and return the home images and their hyperlinks as dictionary.
    If the configuration is already loaded the return from global context otherwise read the config file and load
    images values.
    """

    try:
        if g.home_image_items:
            log.debug("Home images are already loaded.")
    except AttributeError:
        log.debug("Home images are yet to be loaded. Loading from configuration.")

        ngds_home_image_config_path = config.get('ngds.home_images_config_path')

        import ConfigParser
        import os

        if os.path.exists(ngds_home_image_config_path):
            cfgparser = ConfigParser.SafeConfigParser()
            cfgparser.readfp(open(ngds_home_image_config_path))
            section = 'ngds:images'
            if cfgparser.has_section(section):
                image_items = dict(cfgparser.items(section))

            if image_items:
                image_direcotry = config.get('ngds.home_images_dir', 'assets')

                prepend_str = "/" + image_direcotry + "/"

                def transform(multilevelDict):
                    return dict((prepend_str + str(key), (transform(value) if isinstance(value, dict) else value)) for
                                key, value in multilevelDict.items())

                g.home_image_items = transform(image_items)

    return g.home_image_items

def get_filtered_items(request_params):
    """
    Returns the filtered fields in the search results of library page. This method will get called when CKAN doesn't
    return the filtered items(inconsistency in CKAN group/organization view). Request params are checked for filter
    criteria and added to the filter.
    """
    fields_grouped = {}
    for (param, value) in request_params.items():
        if param not in ['q', 'page', 'sort'] \
                and len(value) and not param.startswith('_') and not param.startswith('ext_'):
            if param not in c.fields_grouped:
                fields_grouped[param] = [value]
            else:
                fields_grouped[param].append(value)
    return fields_grouped
