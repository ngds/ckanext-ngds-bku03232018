''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

"""
Handles the functionality of updating/merging the resource details as part of Bulk Upload process. Updates dict value with
respect to the existing and new field values populated for a particular resource.
"""

import copy
import ckanext.importlib.loader as loader
from ckanext.importlib.loader import LoaderError
from ckanclient import CkanApiError, CkanApiNotAuthorizedError
from ckan.plugins import toolkit
import os

log = __import__("logging").getLogger(__name__)

class ResourceLoader(loader.ResourceSeriesLoader):
    """
    Loader finds package based on a specified field and checks to see
    if most fields (listed in field_keys_to_expect_invariant) match the
    pkg_dict. Loader then inserts the resources in the pkg_dict into
    the package and updates any fields that have changed (e.g. last_updated).
    It checks to see if the particular resource is already in the package
    by a custom resource ID which is contained in the description field,
    as a word containing the given prefix.
    """

    def __init__(self, ckanclient,field_keys_to_find_pkg_by,resource_dir=None):
        super(ResourceLoader, self).__init__(ckanclient,field_keys_to_find_pkg_by)
        self.resource_dir = resource_dir



    def _write_package(self, pkg_dict, existing_pkg_name, existing_pkg=None):
        '''
        Writes a package (pkg_dict). If there is an existing package to
        be changed, then supply existing_pkg_name. If the caller has already
        got the existing package then pass it in, to save getting it twice.

        May raise LoaderError or CkanApiNotAuthorizedError (which implies API
        key is wrong, so stop).
        '''
        try:
            pkg_dict = self._update_resource(pkg_dict)
        except LoaderError, ex:
            log.error(ex)
            raise
        except Exception, e:
            log.error(e)
            raise LoaderError('Could not update resources Exception: %s' % e)

        super(ResourceLoader, self)._write_package(pkg_dict, existing_pkg_name, existing_pkg)

    def _update_resource(self, pkg_dict):

        """
        Updates the resource dictionary with uploaded File URL and content model's valid URI and versions.
        If a resource is defined with file to be uploaded in 'upload_file' field then that file is uploaded in CKAN and
        the URL of the file is updated in resource dictionary. If the content_model is defined then content model URI
        and versions are retrieved and updated in the resource dict.
        """

        if pkg_dict.get('resources') is None:
            return pkg_dict

        for resource in pkg_dict['resources']:

            log.debug("Before processing: %s", resource)

            if resource.get('upload_file'):
                try:

                    file_path = os.path.join(self.resource_dir, resource['upload_file'])

                    uploaded_file_url, dummy = self.ckanclient.upload_file(file_path)

                    resource['url'] = uploaded_file_url
                    del resource['upload_file']

                    if resource.get('content_model'):
                        log.debug("Inside content_model....")
                        resource['content_model_uri'], resource['content_model_version'] = self.validate_content_model(resource['content_model'], resource.get('content_model_version'))
                        del resource['content_model']

                except CkanApiNotAuthorizedError:
                    raise
                except CkanApiError:
                    raise LoaderError(toolkit._('Error (%s) uploading file over API: %s') % (self.ckanclient.last_status,self.ckanclient.last_message))
                except Exception, e:
                    print "Error Accessing:", e
                    raise
            else:
                if resource.get('content_model') or resource.get('content_model_version'):
                    raise LoaderError(toolkit._("Content Model referenced but no file referenced for upload. Package Title: %s") % pkg_dict.get('title'))

            self.validate_resource(resource)

        return pkg_dict


    def _merge_resources(self, existing_pkg, pkg):
        """
        Takes an existing_pkg and merges in resources from the pkg.
        """

        if existing_pkg["resources"] == [] :
            log.info("As existing resources are empty passing the package resource as new resources.")
            return pkg.copy()

        # check invariant fields aren't different
        warnings = []
        for key in self.field_keys_to_expect_invariant:
            if key in existing_pkg or key in pkg:
                if (existing_pkg.get(key) or None) != (pkg.get(key) or None):
                    warnings.append('%s: %r -> %r' % (key, existing_pkg.get(key), pkg.get(key)))
            else:
                if (existing_pkg['extras'].get(key) or None) != (pkg['extras'].get(key) or None):
                    warnings.append('%s: %r -> %r' % (key, existing_pkg['extras'].get(key), pkg['extras'].get(key)))
                
        if warnings:
            log.warn('Warning: uploading package \'%s\' and surprised to see '
                     'changes in these values:\n%s' % (existing_pkg['name'], 
                                                       '; '.join(warnings)))

        # copy over all fields but use the existing resources
        merged_dict = pkg.copy()
        merged_dict['resources'] = copy.deepcopy(existing_pkg['resources'])

        if pkg.get('resources') is None:
            return merged_dict        

        # merge resources
        for pkg_res in pkg['resources']:
            # look for resource ID already being there
            pkg_res_id = self._get_resource_id(pkg_res)
            for i, existing_res in enumerate(merged_dict['resources']):
                res_id = self._get_resource_id(existing_res)
                if res_id == pkg_res_id:
                    # edit existing resource
                    merged_dict['resources'][i] = pkg_res
                    break
            else:
                # insert new res
                merged_dict['resources'].append(pkg_res)

        return merged_dict    

    def _get_resource_id(self, res):
        """
        Currently resource name is considered as an unique id (resource id) to determine whether that resource already
        exists in that package.
        """

        return res.get('name')

    def validate_resource(self, resource_dict):
        """
        Calls the validate resource action to check whether constructed resource is valid. If not valid then raises
        validation failure exception.
        """

        validation_response = toolkit.get_action("validate_resource")(None, resource_dict)

        validation_status = validation_response['success']

        if validation_status:
            return True
        else:
            error_msg = '\n'.join(map(str, validation_response['messages']))

            raise LoaderError(toolkit._("Resource validation Failed due to : %s") % error_msg)


    def validate_content_model(self, content_model, version):
        """
        Calls content model validation action.
        """

        #Validatation method needs to be called.
        cm_dict = {'content_model':content_model,'version':version}
        return  toolkit.get_action("contentmodel_checkBulkFile")(None, cm_dict)



