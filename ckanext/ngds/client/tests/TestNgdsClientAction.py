import ckanext.ngds.client.logic.action as ngdsClientAction
import ckan.tests as tests
import ckan.model as model
import paste.fixture
import pylons.test
import ConfigParser
import os
import uuid

class TestNgdsClientAction(object):

    #setup_class executes (auto once) before anything in this class
    @classmethod
    def setup_class(self):
        print ("")

        # get config options
        config = ConfigParser.RawConfigParser({
            'ckan_web_map_service_url': '',
        })
        config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'tests_config.cfg'))

        self.serviceUrl = config.get('tests', 'ckan_web_map_service_url')

        if not self.serviceUrl:
            raise Exception('You must provide WebMapServer URL to the tests '
                            ' configuration file')

        self.actions = ngdsClientAction

        # Make the Paste TestApp that we'll use to simulate HTTP requests to CKAN.
        self.app = paste.fixture.TestApp(pylons.test.pylonsapp)

        # Access CKAN's model directly (bad) to create a sysadmin user and save
        # it against self for all test methods to access.
        self.sysadmin_user = model.User(name='test_sysadmin', sysadmin=True)
        model.Session.add(self.sysadmin_user)
        model.Session.commit()
        model.Session.remove()

        #Create organization
        organization = {'name': 'test_org',
                    'title': 'Maroc',
                    'description': 'Roger likes these books.'}

        resultOrg = tests.call_action_api(self.app, 'organization_create', apikey=self.sysadmin_user.apikey, **organization)

	self.orgID = resultOrg['id']

        #Create Dataset and tied it to created org
        dataset = {'name': 'test_org_dataset',
                   'title': 'A Novel By Tolstoy',
                   'owner_org': organization['name']}

        resultDataset = tests.call_action_api(self.app, 'package_create',
                              apikey=self.sysadmin_user.apikey,
                              **dataset)

	self.datasetID = resultDataset['id']

        #Create Resource and tied it to created dataset
        resource = {'package_id': resultDataset['id'], 'url': self.serviceUrl}
        resultResource = tests.call_action_api(self.app, 'resource_create',
                              apikey=self.sysadmin_user.apikey,
                              **resource)

        #save resource id
        self.resourceID = resultResource['id']

    #teardown_class executes (auto once) after anything in this class
    @classmethod
    def teardown_class(self):
        print ("")

	#Delete Resource created for test
        tests.call_action_api(self.app, 'resource_delete',
                              apikey=self.sysadmin_user.apikey,
                              **{'id': self.resourceID})

        #Delete Dataset created for test
        tests.call_action_api(self.app, 'package_delete',
                              apikey=self.sysadmin_user.apikey,
                              **{'id': self.datasetID})

        #delete Org created
        tests.call_action_api(self.app, 'organization_delete',
                              apikey=self.sysadmin_user.apikey,
                              **{'id': self.orgID})

        model.repo.rebuild_db()

        self.actions = None
        self.resourceID = None
        self.app = None
        self.sysadmin_user = None
        self.serviceUrl = None
        del self.actions
        del self.resourceID
        del self.app
        del self.sysadmin_user
        del self.serviceUrl

    #setup executes before each method in this class
    def setup(self):
        print ("")
        print ("TestUM:setup() before each test method")

    #setup executes after each method in this class
    def teardown(self):
        print ("")
        print ("TestUM:teardown() after each test method")

    #test ngdsClient logic geothermal_prospector_url method
    def test_geothermalProspectorUrl(self):
        print 'test_geothermalProspectorUrl(): Running actual test code ..........................'

        #context = {'model': model,
        #           'session': model.Session,
        #           'user': self.sysadmin_user}

        context = {'user': self.sysadmin_user.name}
        result = self.actions.geothermal_prospector_url(context, {'id': self.resourceID})

	assert result is not 'error'

    #Test Bad ngdsClient logic geothermal_prospector_url method
    def testBad_geothermalProspectorUrl(self):
        print 'testBad_geothermalProspectorUrl(): Running actual test code ..........................'

        context = {'user': self.sysadmin_user.name}
        result = self.actions.geothermal_prospector_url(context, {'id': str(uuid.uuid4())})

        assert result == 'error'
