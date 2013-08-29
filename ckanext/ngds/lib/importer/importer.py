"""
Responsible for handling bulk-upload process. Loads all the data required for
"""
from sqlalchemy.util import OrderedDict

import ckan.model as model
from ckanext.importlib.importer import *
import ckanext.importlib.spreadsheet_importer as spreadsheet_importer

import ckanext.ngds.lib.importer.helper as import_helper
from pylons import config
#the following needs to be revisted and removed...
from ckanext.ngds.metadata.controllers.transaction_data import dispatch as trans_dispatch
from ckanext.ngds.ngdsui.misc import helpers as ui_helper

log = __import__("logging").getLogger(__name__)

#Need to decide our own Read only keys
readonly_keys = ('id', 'revision_id',
                 'relationships',
                 'license',
                 'ratings_average', 'ratings_count',
                 'ckan_url',
                 'metadata_modified',
                 'metadata_created',
                 'notes_rendered')

referenced_keys = ('data_type', 'status', 'protocol')

responsible_party_keys = ('authors', 'maintainer', 'distributor')

date_keys = ('publication_date')


DEFAULT_GROUP = ui_helper.get_default_group()


class BulkUploader(object):

    def __init__(self,client_config=None):

        if client_config is None:
            client_config_file = config.get('ngds.client_config_file')
        else:
            client_config_file = client_config
        #print "client_config_file: ",client_config_file
        self._loadclientconfig(client_config_file)
        self.ckanclient = self._get_ckanclient()


    def _loadclientconfig(self,config_path):
        """
        Loads the client config file which contains the details about server and api key for accessing the server
        functions.
        """
        import ConfigParser
        import os
        import urlparse
        if os.path.exists(config_path):
            cfgparser = ConfigParser.SafeConfigParser()
            cfgparser.readfp(open(config_path))
            section = 'app:client'
            if cfgparser.has_section(section):
                self.url = cfgparser.get(section, 'api_url', '')
                #print "self.url: ",self.url
                if self.url =='':
                        #print "API URL is None so can't proceed further"
                        raise Exception ("Unable to find API URL or URL is empty")
                self.parsed = urlparse.urlparse(self.url)
                newparsed = list(self.parsed)
                self.netloc = self.parsed.netloc            
                section = 'index:%s' % self.netloc
                if cfgparser.has_section(section):
                    self.api_key = cfgparser.get(section, 'api_key', '')                
                    if self.api_key =='':
                        #print "API URL is None so can't proceed further"
                        raise Exception ("Unable to find API key or API key is empty.")                        
            else:                        
                raise Exception ("Unable to find API URL or URL is empty")

        else:
            #print "Unable to find the client configuration file."
            raise Exception ("Unable to find the client config file.")

    
    def _get_ckanclient(self):
        """
        Returns NGDS Ckan client.
        """

        from ckanext.ngds.lib.client import NgdsCkanClient

        testclient = NgdsCkanClient(base_location=self.url, api_key=self.api_key)

        return testclient

    def execute_bulk_upload(self):
        """
        This method will get all the bulk uploaded records with the status of "VALID" and process them. 
        If it can process the records successfully then updates the status as "Completed" otherwise as "Failure" and corresponding comments.
        """        
        import os
        log.debug("entering execute_bulk_upload")
        query = model.BulkUpload.search("VALID")

        for bulk_upload_record in query.all():

            log.debug("Processing the file: %s", bulk_upload_record.data_file)

            try:
                data_file_path = os.path.join(bulk_upload_record.path,bulk_upload_record.data_file)
                self.importpackagedata(bulk_upload_record.id,file_path=data_file_path,resource_dir=bulk_upload_record.path,ckanclient=self.ckanclient)
                bulk_upload_record.status = "COMPLETED"
            except Exception, e:
                log.debug(e)
                log.debug("Exception while processing bulk upload for the file : %s" , bulk_upload_record.data_file )
                bulk_upload_record.status = "FAILURE"
                bulk_upload_record.comments = e.message
            finally:
                import_helper.delete_files(file_path=bulk_upload_record.path,ignore_files=[bulk_upload_record.data_file,bulk_upload_record.resources])
                bulk_upload_record.last_updated = None
                bulk_upload_record.save()


    def importpackagedata(self,bulk_upload_id,file_path=None,resource_dir=None,ckanclient=None):
        """
        This is an entry point for bulk upload of one record(bulk uploaded template). Loads the package details as
        dict from xls file and loads them into CKAN. Each successfully loaded pacakges are referenced against bulk upload
        record for tracking.
        """
        from ckan.lib.navl.dictization_functions import DataError, unflatten, validate
        from ckan.logic import (tuplize_dict,clean_dict,parse_params,flatten_to_string_key)

        
        from ckanext.ngds.lib.importer.loader import ResourceLoader

        if ckanclient is None:
            ckanclient = self._get_ckanclient()

        loader = ResourceLoader(ckanclient,field_keys_to_find_pkg_by=['name'],resource_dir=resource_dir)
          
        package_import = NGDSPackageImporter(filepath=file_path)

        pkg_dicts = [pkg_dict for pkg_dict in package_import.pkg_dict()]

        for pkg_dict in pkg_dicts:
            try:
                returned_package = loader.load_package(clean_dict(unflatten(tuplize_dict(pkg_dict))))
                # Upload bulk upload to package relationship.
                self._create_bulk_upload_package(bulk_upload_id,returned_package['name'],returned_package['title'])

            except Exception , e:
                log.info(e)
                log.info("Skipping this record and proceeding with next one....")
                raise
    
    def _create_bulk_upload_package(self,bulk_upload_id, package_name, package_title):
        """
        Creates DB entry in 'bulk_upload_package' table for linking bulk upload and uploaded package.
        """
        log.debug("Create Bulk Upload Package: bid: %s pname: %s  ptitle: %s" % (bulk_upload_id, package_name, package_title))
        data = {'bulk_upload_id': bulk_upload_id, 'package_name': package_name, 'package_title': package_title}
        data_dict = {'model': 'BulkUpload_Package'}
        data_dict['data'] = data
        data_dict['process'] = 'create'
        context = {'model': model, 'session': model.Session}   
        trans_dispatch(context, data_dict)


class SpreadsheetDataRecords(DataRecords):
    '''Takes SpreadsheetData and converts it its titles and
    data records. Handles title rows and filters out rows of rubbish.
    '''
    def __init__(self, spreadsheet_data, essential_title):
        assert isinstance(spreadsheet_data, spreadsheet_importer.SpreadsheetData), spreadsheet_data
        self._data = spreadsheet_data
        self.titles, self.last_titles_row_index = self.find_titles(essential_title)
        self._first_record_row = self.find_first_record_row(self.last_titles_row_index + 1)     

    def find_titles(self, essential_title):
        row_index = 0
        titles = []
        essential_title_lower = essential_title.lower()
        while True:
            if row_index >= self._data.get_num_rows():
                raise ImportException('Could not find title row')
            row = self._data.get_row(row_index)
            if essential_title in row or essential_title_lower in row:
                for row_val in row:
                    titles.append(row_val.strip() if isinstance(row_val, basestring) else None)
                return (titles, row_index)
            row_index += 1

    def find_first_record_row(self, row_index_to_start_looking):
        row_index = row_index_to_start_looking
        while True:
            if row_index >= self._data.get_num_rows():
                raise ImportException('Could not find first record row')
            row = self._data.get_row(row_index)

            if not (u'<< Datasets Displayed Below' in row or\
                    row[:5] == [None, None, None, None, None] or\
                    row[:5] == ['', '', '', '', '']\
                    ):
                return row_index
            row_index += 1

    @property
    def records(self):
        '''Returns each record as a dict.'''
        for row_index in range(self._first_record_row, self._data.get_num_rows()):
            row = self._data.get_row(row_index)
            row_has_content = False
            for cell in row:
                if cell:
                    row_has_content = True
                    break
            if row_has_content:
                record_dict = OrderedDict(zip(self.titles, row))
                if record_dict.has_key(None):
                    del record_dict[None]
                yield record_dict

class NGDSPackageImporter(spreadsheet_importer.SpreadsheetPackageImporter):
    '''From a filepath of an Excel or csv file, extracts package
    dictionaries.'''
    def __init__(self, record_params=None, record_class=SpreadsheetDataRecords, **kwargs):
        self._record_params = record_params if record_params != None else ['Title']
        self._record_class = record_class
        super(NGDSPackageImporter, self).__init__(record_class=record_class,**kwargs)

    @classmethod
    def license_2_license_id(self, license_title, logger=None):
        """
        """

        # import is here, as it creates a dependency on ckan, which many importers won't want
        from ckan.model.license import LicenseRegister
        licenses = LicenseRegister()
        license_obj = licenses.get(license_title)

        if license_obj:
            return u'%s' % license_obj.id
        else:
            log.warn('Warning: No license name matches %s. Ignoring license.' % license_title)
            return u''

    @classmethod
    def responsible_party_2_id(self,name,email):
        """
        TODO: Need
        """

        from ckan.model import ResponsibleParty

        resparty = ResponsibleParty()

        foundparties = (resparty.find(email)).all()

        numberofResParties = lenNee(foundparties)

        if numberofResParties == 0:
            raise Exception("Data Error: No responsible party is found with the given name %s and email %s " % (name,email))
            #Need to add this person into Responsible Party details.
        elif numberofResParties > 1:
            raise Exception("Data Error: More than one responsible party is found with the given name %s and email %s " % (name,email))
        else:
            log.debug("Found Party ID: %s",numberofResParties[0].id)
            return numberofResParties[0].id

    @classmethod
    def validate_SD(self,model_type,sdValue):
        """
        Validates whether any referenced data field exists in the Standing Data (Reference base table) table. If not
        raises Exception.
        """

        #Call Model's validate method which will compare the sd value against the Standing data table.
        from ckanext.ngds.env import ckan_model

        sdObject = ckan_model.StandingData()

        validated_value = sdObject.validate(model_type, sdValue)

        if validated_value is None:
            raise Exception("Data Error: No Standing data matching the input - %s for the type - %s" % (sdValue,model_type)) 
        else:
            return validated_value

    @classmethod
    def validate_responsible_party(cls, field_name, email_string):
        """
        Validates whether the input responsible party details already exists in the system.(Authors, maintainer and
        distributor are considered as Responsible Parties). Authors is a multi-valued field, hence separated by comma.
        If doesn't exist then raises validation Exception, otherwise returns the responsible party details as Json.
        """

        from ckanext.ngds.env import ckan_model

        email_list = [x.strip() for x in str(email_string).split(',') if x.strip()]

        if len(email_list) > 1 and field_name.lower() != 'authors':
            raise Exception("Data Error: %s can not have more than one person" % field_name)

        party_list = []

        for email in email_list:

            returned_party = ckan_model.ResponsibleParty.find(email.lower()).all()

            if returned_party and len(returned_party) > 0:
                user_dict = {}
                user_dict['name'] = returned_party[0].name
                user_dict['email'] = returned_party[0].email
                party_list.append(user_dict)
            else:
                raise Exception("Responsible party with email: %s not found in the system. Please add either manually or use loader script." % email)

        import json
        if field_name.lower() == 'authors':
            return json.dumps(party_list)
        else:
            return json.dumps(party_list[0])

    @classmethod
    def get_iso_date_string(cls, field_name, cell):

        return None

    @classmethod
    def pkg_xl_dict_to_fs_dict(cls, pkg_xl_dict, logger=None):
        '''Convert a Package represented in an Excel-type dictionary to a
        dictionary suitable for fieldset data.
        Takes Excel-type dict:
            {'name':'wikipedia', 
             'resource-0-url':'http://static.wikipedia.org/'}
        Returns Fieldset-type dict:
            {'name':'wikipedia',
             'resources':[{'url':'http://static.wikipedia.org/'}]}
        '''

        standard_fields = model.Package.get_fields()

        pkg_fs_dict = OrderedDict()
        for title, cell in pkg_xl_dict.items():
            #log.debug("title:%s, value: %s" % (title,cell))
            if cell:
                if title in referenced_keys:
                    cell = cls.validate_SD(title,cell)
                if title in responsible_party_keys:
                    cell = cls.validate_responsible_party(title, cell)

                if title in date_keys:
                    cell = cls.get_iso_date_string(title,cell)

                if title == 'tags':
                    pkg_fs_dict['tag_string'] = cell
                elif title in standard_fields:
                    pkg_fs_dict[title] = cell
                elif title == 'license':
                    #print "license: ", cell
                    license_id = cls.license_2_license_id(cell)
                    #print "license_id: ",license_id
                    if license_id:
                        pkg_fs_dict['license_id'] = license_id
                    else:
                        logger('Warning: No license name matches \'%s\'. Ignoring license.' % cell)
                elif title.startswith('resource-'):
                    match = re.match('resource-(\d+)-(\w+)', title)
                    if match:
                        res_index, field = match.groups()
                        res_index = int(res_index)
                        field = str(field)
                        if field in referenced_keys:
                            cell = cls.validate_SD(field,cell)
                        if field in responsible_party_keys:
                            cell = cls.validate_responsible_party(field, cell)
                        if not pkg_fs_dict.has_key('resources'):
                            pkg_fs_dict['resources'] = []
                        resources = pkg_fs_dict['resources']
                        num_new_resources = 1 + res_index - len(resources)
                        for i in range(num_new_resources):
                            blank_dict = OrderedDict()
                            for blank_field in model.Resource.get_columns(extra_columns=False):
                                blank_dict[blank_field] = u''
                            pkg_fs_dict['resources'].append(blank_dict)

                        pkg_fs_dict['resources'][res_index][field] = cell
                    else:
                        logger('Warning: Could not understand resource title \'%s\'. Ignoring value: %s' % (title, cell))
                elif title.startswith('relationships'):
                    # TODO
                    pass
                elif title == 'download_url':
                    # deprecated - only in there for compatibility
                    pass
                elif title in readonly_keys:
                    pass
                else:
                    if not pkg_fs_dict.has_key('extras'):
                        pkg_fs_dict['extras'] = {}
                    pkg_fs_dict['extras'][title] = cell
        pkg_fs_dict['owner_org'] = DEFAULT_GROUP
        return pkg_fs_dict