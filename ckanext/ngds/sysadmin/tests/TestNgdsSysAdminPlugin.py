from ckanext.ngds.common import plugins
import ckanext.ngds.sysadmin.plugin as pluginNgdsSysAdmin
import ckanext.ngds.sysadmin.helpers as helper
import ConfigParser
import os
import ckanext.ngds.sysadmin.model.db as db
from ckanext.ngds.common import model
import json

class TestNgdsSysAdminPlugin(object):

    #setup_class executes (auto once) before anything in this class
    @classmethod
    def setup_class(self):
        print ("")
        # get config options
        config = ConfigParser.RawConfigParser({
            'ckan_host': '0.0.0.0',
        })
        config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'tests_config.cfg'))

        self.host = config.get('tests', 'ckan_host')
        self.path = config.get('tests', 'ckan_ngds_sysadmin_search_path')

        if not self.host:
            raise Exception('You must add a Host to the tests '
                            ' configuration file')

        if not self.path:
            raise Exception('You must add a Ngds SysAdmin Search path to the tests '
                            ' configuration file')

	#load sysadmin extension
	plugins.load('ngds_sysadmin')

        self.oNgdsSysAdmin = pluginNgdsSysAdmin.SystemAdministrator()

    #teardown_class executes (auto once) after anything in this class
    @classmethod
    def teardown_class(self):
        print ("")
        self.oNgdsSysAdmin = None
        self.host = None
        self.path = None
        del self.oNgdsSysAdmin
        del self.host
        del self.path

	#unload sysadmin plugin
        plugins.unload('ngds_sysadmin')

    #setup executes before each method in this class
    def setup(self):
        print ("")
        print ("TestUM:setup() before each test method")

    #setup executes after each method in this class
    def teardown(self):
        print ("")
        print ("TestUM:teardown() after each test method")

   #testintg returned methods 'get_helpers' that really exist in helper
    def test_getHelpers(self):
        print 'test_getHelpers(): Running actual test code ..........................'

        result = self.oNgdsSysAdmin.get_helpers()
	listMethods = dir(helper)

        for name in result:
            assert name in listMethods

    #testing ngds_homepage_search view is up and the response status code is 200
    def test_ngdsHomepageSearch(self):
        print 'test_ngdsHomepageSearch(): Running actual test code ..........................'

        import requests
        query = 'query=&search-type=catalog_search'
        try:
            oResponse = requests.post("http://%s%s?%s" % (self.host, self.path, query))
            assert oResponse.status_code == 200
        except requests.ConnectionError:
            print "failed to connect"
            assert False

    #test changed config value on loading sysadmin plugin using Model/db method
    def test_overriddenConfigValue(self):

        dbConfig = db.init_config_show(model)

        assert 'ngds.publish' in dbConfig
        assert 'ngds.harvest' in dbConfig
        assert 'ngds.edit_metadata' in dbConfig

        assert json.dumps(dbConfig['ngds.publish']).strip('"') == 'True'
        assert json.dumps(dbConfig['ngds.harvest']).strip('"') == 'True'
        assert json.dumps(dbConfig['ngds.edit_metadata']).strip('"') == 'True'
