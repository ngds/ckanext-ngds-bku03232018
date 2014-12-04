import ckanext.ngds.client.plugin as ngdsClientPlugin
import ConfigParser
import os
import ast

class TestNgdsClientPlugin(object):

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
        self.paths = ast.literal_eval(config.get('tests', 'ckan_ngds_client_paths'))

        if not self.host:
            raise Exception('You must add a Host to the tests '
                            ' configuration file')

        if not self.paths:
            raise Exception('You must add a Ngds client paths to the tests '
                            ' configuration file')

        self.oNgdsClientPlugin = ngdsClientPlugin.NGDSClient()

    #teardown_class executes (auto once) after anything in this class
    @classmethod
    def teardown_class(self):
        print ("")
        self.oNgdsClientPlugin = None
        self.host = None
        self.paths = None
        del self.oNgdsClientPlugin
        del self.host
        del self.paths

    #setup executes before each method in this class
    def setup(self):
        print ("")
        print ("TestUM:setup() before each test method")

    #setup executes after each method in this class
    def teardown(self):
        print ("")
        print ("TestUM:teardown() after each test method")

    #Test the method get_actions of NgdsClientPlugin Class return the {'geothermal_prospector_url'}
    def test_getActions(self):
        print 'test_getActions(): Running actual test code ..........................'

        result = self.oNgdsClientPlugin.get_actions()

        assert 'geothermal_prospector_url' in result

    #Test client ngds plugin is up and the response status code for all paths (routes) is 200
    def test_ngdsClientUrls(self):
        print 'test_ngdsClientUrls(): Running actual test code ..........................'

        import requests
        try:
	    for route in self.paths:
                oResponse = requests.head("http://%s%s" % (self.host, route))
                assert oResponse.status_code == 200

        except requests.ConnectionError:
            print "failed to connect"
            assert False
