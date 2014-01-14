''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

from ckan.plugins import implements, SingletonPlugin, IRoutes, IConfigurer, toolkit, IAuthFunctions, IFacets, \
    ITemplateHelpers, IPackageController, IConfigurable, IActions, IDatasetForm

from ckan.lib.base import (model, g)

from ckanext.ngds.ngdsui.misc import helpers
from ckanext.ngds.ngdsui.lib.poly import get_package_ids_in_poly
from ckanext.ngds.ngdsui import authorize

import ckanext.datastore.logic.auth as datastore_auth
import ckanext.ngds.contentmodel.model.contentmodels as contentmodels
import ckanext.ngds.contentmodel.logic.action as contentmodel_action
import ckanext.ngds.logic.action.validate as ngds_validator

from pylons import config as ckan_config

import sys
import re

try:
    from collections import OrderedDict # 2.7
except ImportError:
    from sqlalchemy.util import OrderedDict


class NgdsuiPlugin(SingletonPlugin, toolkit.DefaultDatasetForm):
    def customize_ckan_for_ngds(self):
        """
        Load ckan's authorization module and update the default role with NGDS specific roles.
        """

        #helpers.get_contributors_list()

        def _trans_role_datasteward():
            return ('Data Steward')

        def _trans_role_datasubmitter():
            return ('Data Submitter')

        module_obj = sys.modules['ckan.new_authz']

        #Create this new module methods for new roles. 'admin' and 'member' already exists in the default roles.
        setattr(module_obj, '_trans_role_datasteward', _trans_role_datasteward)
        setattr(module_obj, '_trans_role_datasubmitter', _trans_role_datasubmitter)

        from ckan import new_authz

        # Initialise NGDS roles.
        new_authz.ROLE_PERMISSIONS = OrderedDict([
            ('admin', ['admin']),
            ('datasteward', ['read', 'delete_dataset', 'create_dataset', 'update_dataset', 'publish_dataset']),
            ('datasubmitter', ['read', 'create_dataset', 'update_dataset']),
            ('member', ['read']),
        ])


    def create_default_group(self, data_dict=None):
        group = model.Group.get('public')

        print group

        if group:
            print "success "
        else:
            print "fail"

            # data_dict['name'] = 'default'
            # data_dict['type'] = 'organization'
            # context= {}
            # data_dict['users'] = [{'name': 'admin', 'capacity': 'admin'}]
            # get_action('group_create')(context, data_dict)

    def contentmodel_configure(self, config):
        if "usgin_url" in config:
            contentmodels.usgin_url = config["usgin_url"]
        else:
            contentmodels.usgin_url = "http://schemas.usgin.org/contentmodels.json"
            # Access the URL and fill the cache
        print "Caching Content Models from USGIN: " + contentmodels.usgin_url
        contentmodel_action.contentmodel_refreshCache(None, None)

        True_List = ["true", "1", "t", "y", "yes", "yeah", "yup", "certainly"]

        if "checkfile_maxerror" in config:
            try:
                checkfile_maxerror = config["checkfile_maxerror"]
                contentmodels.checkfile_maxerror = int(checkfile_maxerror)
            except:
                print "DON'T UNDERSTAND the 'checkfile_maxerror' in the development.ini, it is not an Integer"
        print "checkfile_maxerror", contentmodels.checkfile_maxerror

        if "checkfile_checkheader" in config:
            try:
                checkfile_checkheader = config["checkfile_checkheader"]
                if checkfile_checkheader in True_List:
                    contentmodels.checkfile_checkheader = True
                else:
                    contentmodels.checkfile_checkheader = False
            except:
                print "DON'T UNDERSTAND the 'checkfile_checkheader' in the development.ini, it is not a boolean string"
        print "checkfile_checkheader", contentmodels.checkfile_checkheader

        if "checkfile_checkoptionalfalse" in config:
            try:
                checkfile_checkoptionalfalse = config["checkfile_checkoptionalfalse"]
                if checkfile_checkoptionalfalse in True_List:
                    contentmodels.checkfile_checkoptionalfalse = True
                else:
                    contentmodels.checkfile_checkoptionalfalse = False
            except:
                print "DON'T UNDERSTAND the 'checkfile_checkoptionalfalse' in the development.ini, it is not a boolean string"
        print "checkfile_checkoptionalfalse", contentmodels.checkfile_checkoptionalfalse

    implements(IConfigurable, inherit=True)

    def configure(self, config):
        self.contentmodel_configure(config)

    implements(IRoutes, inherit=True)

    def before_map(self, map):
        """
        For the moment, set up routes under the sub-root /ngds to render the UI.
        """
        home_controller = "ckanext.ngds.ngdsui.controllers.home:HomeController"
        map.connect("home", "/", controller=home_controller, action="render_index", conditions={"method": ["GET"]})
        map.connect("ngds_home", "/ngds", controller=home_controller, action="render_index",
                    conditions={"method": ["GET"]})
        map.connect("initiate_search", "/ngds/initiate_search", controller=home_controller, action="initiate_search",
                    conditions={"method": ["POST"]})
        map.connect("about", "/ngds/about", controller=home_controller, action="render_about",
                    conditions={"method": ["GET"]})

        contribute_controller = "ckanext.ngds.ngdsui.controllers.contribute:ContributeController"
        map.connect("contribute", "/ngds/contribute", controller=contribute_controller, action="index")
        map.connect("create_or_update_resource", "/ngds/contribute/create_or_update_resource",
                    controller=contribute_controller, action="create_or_update_resource",
                    conditions={"method": ["POST"]})
        map.redirect('/ngds/contribute/dataset/{action}', '/dataset/{action}')
        map.connect("bulk_upload", "/ngds/bulk_upload", controller=contribute_controller, action="bulk_upload")
        map.connect("bulk_upload_handle", "/ngds/bulk_upload_handle", controller=contribute_controller,
                    action="bulk_upload_handle")

        map.connect("bulk_upload_list", "/ngds/bulkupload_list", controller=contribute_controller,
                    action="bulkupload_list")
        map.connect("bulk_upload_package", "/ngds/bulkupload_package", controller=contribute_controller,
                    action="bulkupload_package_list")
        map.connect("execute_bulkupload", "/ngds/execute_bulkupload", controller=contribute_controller,
                    action="execute_bulkupload")

        map.connect("rating_submit", "/ngds/rating_submit", controller=home_controller, action="rating_submit",
                    conditions={"method": ["POST"]})
        map.connect("save_search", "/ngds/save_search", controller=home_controller, action="save_search",
                    conditions={"method": ["POST"]})

        #Map related paths
        map.connect("map", "/ngds/map", controller=home_controller, action="render_map", conditions={"method": ["GET"]})
        map.connect("library", "/ngds/library", controller=home_controller, action="render_library",
                    conditions={"method": ["GET"]})
        map.connect("resources", "/ngds/resources", controller=home_controller, action="render_resources",
                    conditions={"method": ["GET"]})
        map.redirect("search", "/ngds/library/search", "/dataset", highlight_actions='index search')

        user_controller = "ckanext.ngds.ngdsui.controllers.user:UserController"

        map.connect("manage_users", "/ngds/users", controller=user_controller, action="manage_users")
        map.connect("member_new", "/ngds/member_new", controller=user_controller, action="member_new")
        map.connect("logout_page", "/user/logged_out_redirect", controller=user_controller, action="logged_out_page")
        map.connect("execute_fulltext_indexer", "/ngds/execute_fulltext_indexer", controller=contribute_controller,
                    action="execute_fulltext_indexer")

        #Help related paths

        #Footer URLS
        map.connect("partners", "/ngds/partners", controller=home_controller, action="render_partners")
        map.connect("data", "/ngds/data", controller=home_controller, action="render_data")
        map.connect("history", "/ngds/history", controller=home_controller, action="render_history")
        map.connect("developers", "/ngds/develop", controller=home_controller, action="render_developers")
        map.connect("new_to_ngds", "/ngds/new_to_ngds", controller=home_controller, action="render_new_to_ngds")
        map.connect("faq", "/ngds/faq", controller=home_controller, action="render_faq")
        map.connect("contributors_list", "/ngds/contributors_list", controller=home_controller,
                    action="render_contributors")
        map.connect("contributors_list", "/ngds/terms_of_use", controller=home_controller, action="render_terms_of_use")
        map.connect("contributors_list", "/ngds/contact", controller=home_controller, action="render_contact")
        map.connect("rate", "/ngds/rate/{pkg_id}/{rating_value}", controller=home_controller, action="rate")
        return map

    implements(IConfigurer, inherit=True)

    def update_config(self, config):
        """
        Register the templates directory with ckan so that Jinja can find them.
        """
        toolkit.add_template_directory(config, 'templates')
        #Static files are to be served up from here. Otherwise, pylons will try and decode content in here and will fail.
        toolkit.add_public_directory(config, 'public')

        self.customize_ckan_for_ngds()

    implements(IActions, inherit=True)

    def get_actions(self):
        return {
            'contentmodel_refreshCache': contentmodel_action.contentmodel_refreshCache,
            'contentmodel_list': contentmodel_action.contentmodel_list,
            'contentmodel_list_short': contentmodel_action.contentmodel_list_short,
            'contentmodel_get': contentmodel_action.contentmodel_get,
            'contentmodel_checkFile': contentmodel_action.contentmodel_checkFile,
            'contentmodel_checkBulkFile': contentmodel_action.contentmodel_checkBulkFile,
            'get_content_models_for_ui': helpers.get_content_models_for_ui_action,
            'get_content_model_version_for_uri': helpers.get_content_model_version_for_uri_action,
            'get_better_package_info': helpers.make_better_json

            #'create_resource_document_index': lib_action.create_resource_document_index
            # 'validate_resource': validate_action.validate_resource,
            # 'validate_dataset_metadata':validate_action.validate_dataset_metadata
        }

    implements(IAuthFunctions, inherit=True)

    def get_auth_functions(self):

        return {
            'manage_users': authorize.manage_users,
            'publish_dataset': authorize.publish_dataset,
            'manage_nodes': authorize.manage_nodes,
            'execute_bulkupload': authorize.execute_bulkupload,
            'contentmodel_refreshCache': datastore_auth.datastore_create,
            'contentmodel_list': datastore_auth.datastore_create,
            'contentmodel_checkFile': datastore_auth.datastore_create,
        }

    implements(ITemplateHelpers, inherit=True)

    def get_helpers(self):
        return {
            'get_responsible_party_name': helpers.get_responsible_party_name,
            'get_default_group': helpers.get_default_group,
            'get_login_url': helpers.get_login_url,
            'get_language': helpers.get_language,
            'get_url_for_file': helpers.get_url_for_file,
            'is_plugin_enabled': helpers.is_plugin_enabled,
            'username_for_id': helpers.username_for_id,
            'load_ngds_facets': helpers.load_ngds_facets,
            'get_ngdsfacets': helpers.get_ngdsfacets,
            'get_formatted_date': helpers.get_formatted_date,
            'get_formatted_date_from_obj': helpers.get_formatted_date_from_obj,
            'get_field_title': helpers.get_field_title,
            'is_string_field': helpers.is_string_field,
            'is_ogc_publishable': helpers.is_ogc_publishable,
            'jsonify': helpers.jsonify,
            'highlight_rating_star': helpers.highlight_rating_star,
            'count_rating_reviews': helpers.count_rating_reviews,
            'rating_text': helpers.rating_text,
            'get_usersearches': helpers.get_usersearches,
            'get_dataset_category_image_path': helpers.get_dataset_category_image_path,
            'is_following': helpers.is_following,
            'parseJSON': helpers.parseJSON,
            'json_extract': helpers.json_extract,
            'get_master_style': helpers.get_master_style,
            'toJSON': helpers.to_json,
            'split': helpers.split,
            'get_label_for_pkg_attribute': helpers.get_label_for_pkg_attribute,
            'is_json': helpers.is_json,
            'get_label_for_resource_attribute': helpers.get_label_for_resource_attribute,
            'is_development': helpers.is_development,
            'get_rating_details': helpers.get_rating_details,
            'get_top_5_harvest_sources': helpers.get_top_5_harvest_sources,
            'get_home_images': helpers.get_home_images,
            'get_filtered_items': helpers.get_filtered_items,
            'get_content_models': helpers.get_content_models,
            'get_contributors_list': helpers.get_contributors_list,
            'parse_publication_date_range': helpers.parse_publication_date_range,
            'get_content_models_for_ui': helpers.get_content_models_for_ui,
            'get_content_model_versions_for_uri': helpers.get_content_model_versions_for_uri,
            'get_full_resource_dict': helpers.get_full_resource_dict,
            'get_dataset_categories': helpers.get_dataset_categories,
            'get_status_for_ui': helpers.get_status_for_ui,
            'get_languages_for_ui': helpers.get_languages_for_ui,
            'get_cur_page': helpers.get_cur_page,
            'get_cur_page_help': helpers.get_cur_page_help,
            'get_content_model_dict': helpers.get_content_model_dict,
            'metadata_fields_to_display_for_cm': helpers.metadata_fields_to_display_for_cm,
            'get_role_for_username': helpers.get_role_for_username
        }

    implements(IPackageController, inherit=True)

    def before_index(self, pkg_dict):
        #pkg_dict['sample_created']={'prahadeesh':'abclll'}
        is_full_text_enabled = ckan_config.get('ngds.full_text_indexing', 'false')

        file_formats_to_ignore = ('csv')

        import json

        if pkg_dict.get('data_dict'):
            dict = json.loads(pkg_dict.get('data_dict'))
            resources = dict.get('resources')

        #print "resources: ", resources

        if resources:
            document_index_list = []
            for resource in resources:

                res_file_field = 'resource_file_%s' % resource.get("id")
                #print "res_file_field:", res_file_field
                pkg_dict[res_file_field] = ''

                try:
                    for (okey, nkey) in [('distributor', 'res_distributor'),
                                         ('protocol', 'res_protocol'),
                                         ('layer', 'res_layer'),
                                         ('resource_format', 'res_resource_format'),
                                         ('content_model', 'res_content_model')]:
                        pkg_dict[nkey] = pkg_dict.get(nkey, []) + [resource.get(okey, u'')]

                    if is_full_text_enabled == 'true' and resource.get('resource_format', '') == 'unstructured' and \
                                    str(resource.get('format', u'')).lower() not in file_formats_to_ignore:

                        file_path = helpers.file_path_from_url(resource.get("url"))
                        if file_path:
                            resource_index_dict = {'package_id': pkg_dict.get('id'),
                                                   'resource_id': resource.get("id"),
                                                   'file_path': file_path,
                            }
                            document_index_list.append(resource_index_dict)
                except Exception, ex:
                    print "Exception while getting some full text indexing values: %s" % ex

            if is_full_text_enabled == 'true' and document_index_list:
                helpers.create_package_resource_document_index(pkg_dict.get('id'), document_index_list)

        return pkg_dict


    def before_search(self, search_params):

        if 'fq' in search_params or 'q' in search_params:
            def repl(m):
                datestr = m.group()
                datestr = datestr.replace("\"", "")
                return datestr

            if 'fq' in search_params:
                search_params['fq'] = re.sub('publication_date:".*"', repl, search_params['fq'])
            if 'q' in search_params:
                search_params['q'] = re.sub('publication_date: ".*"', repl, search_params['q'])

        if 'extras' in search_params and 'poly' in search_params['extras'] and search_params['extras']['poly']:
            # do some validation
            # We'll perform the existing search but also filtering by the ids
            # of datasets within the bbox
            x = {'poly': search_params['extras']['poly']}
            bbox_query_ids = get_package_ids_in_poly(x, '4326')
            q = search_params.get('q', '')
            new_q = '%s AND ' % q if q else ''
            new_q += '(%s)' % ' OR '.join(['id:%s' % id for id in bbox_query_ids])
            search_params['q'] = new_q
        else:
            print "Definitely not in"

        return search_params

    def after_search(self, search_results, search_params):

        def mark_wms_pkgs(pkg):

            def is_wms_resource(resource):
                if 'protocol' in resource and resource['protocol'].lower() == 'ogc:wms':
                    return True
                return False

            if True in map(is_wms_resource, pkg['resources']):
                pkg['hasWMSResources'] = True

        map(mark_wms_pkgs, search_results['results'])

        try:
            if g.facet_json_data:
                print "global value is there..."
        except AttributeError:
            print "Facet json config is not available. Returning the default facets."
            helpers.load_ngds_facets()
            #print "search_results: ",search_results
        return search_results

    def before_view(self,pkg):
        # pkg['title'] = "Muhaha"
        # print pkg
        # TODO - Use for rendering packages. Process resources to get more responsible party information from the email.
        return pkg

    implements(IFacets, inherit=True)

    def dataset_facets(self, facets_dict, package_type):
        #print "IFACETS is called.......>>>>>>>>>>>>>>>>"

        if package_type == 'harvest':
            return OrderedDict([('frequency', 'Frequency'), ('source_type', 'Type')])

        ngds_facets = helpers.load_ngds_facets()

        if ngds_facets:
            facets_dict = ngds_facets

        return facets_dict

    def organization_facets(self, facets_dict, organization_type, package_type):
        #print "IFACETS is called.......>>>>>>>>>>>>>>>>"

        if package_type == 'harvest':
            return OrderedDict([('frequency', 'Frequency'), ('source_type', 'Type')])

        ngds_facets = helpers.load_ngds_facets()

        if ngds_facets:
            facets_dict = ngds_facets

        return facets_dict

    implements(IDatasetForm)

    def package_types(self):
        return ['dataset']

    def is_fallback(self):
        return False

    def package_form(self):
        return 'package/new_package_form.html'

    def search_template(self):
        return 'package/search.html'

    def read_template(self):
        return 'package/read.html'

    def new_template(self):
        return 'package/new.html'

    def edit_template(self):
        return 'package/edit.html'

    def setup_template_variables(self, context, data_dict):
        toolkit.DefaultDatasetForm().setup_template_variables(context, data_dict)
        return data_dict

    def create_package_schema(self):
        default_schema = super(NgdsuiPlugin, self).create_package_schema()
        return ngds_validator.ngds_create_schema(default_schema)

    def update_package_schema(self):
        default_schema = super(NgdsuiPlugin, self).update_package_schema()
        return ngds_validator.ngds_update_schema(default_schema)

    def show_package_schema(self):
        pass
