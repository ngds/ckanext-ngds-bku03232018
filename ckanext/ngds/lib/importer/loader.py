import re
import copy
import ckanext.importlib.loader as loader
from pprint import pformat

log = __import__("logging").getLogger(__name__)

def importrecordclient(self,file_path="/home/ngds/work/GITHUB/ckanext-importlib/ckanext/importlib/tests/samples/test_importer_full.xls"):
    #print "Entered Import Record Client:",file_path
    from ckan.lib.navl.dictization_functions import DataError, unflatten, validate
    from ckan.logic import (tuplize_dict,clean_dict,parse_params,flatten_to_string_key)

    from ckanclient import CkanClient
    from ckanext.ngds.lib.importer.loader import ResourceLoader

    testclient = CkanClient(base_location='http://localhost:5000/api', api_key="3b81cfec-b3b8-471d-ac50-e722d26c3893")
    loader = ResourceLoader(testclient,field_keys_to_find_pkg_by=['name'])
      
    package_import = NGDSPackageImporter(filepath=file_path)

    pkg_dicts = [pkg_dict for pkg_dict in package_import.pkg_dict()]

    for pkg_dict in pkg_dicts:
        print "Processing Package: ",pkg_dict['title']
        try:
            loader.load_package(clean_dict(unflatten(tuplize_dict(pkg_dict))))
        except Exception , e:
            print "Skipping this record and proceeding with next one....",e 

class ResourceLoader(loader.ResourceSeriesLoader):

    def _merge_resources(self, existing_pkg, pkg):
        '''Takes an existing_pkg and merges in resources from the pkg.
        '''
        #log.info("..Merging resources into %s" % existing_pkg["name"])
        #log.debug("....Existing resources:\n%s" % pformat(existing_pkg["resources"]))
        #log.debug("....New resources:\n%s" % pformat(pkg["resources"]))
        log.info("Entering NGDS merge");

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

        log.debug("....Merged resources:\n%s" % pformat(merged_dict["resources"]))

        return merged_dict    

    #this has to change just for now doing this....
    def _get_resource_id(self, res):
        print "Inside NGDS Resource Loader"
        return res.get('url')