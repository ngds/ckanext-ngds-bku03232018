import csv
import copy

from sqlalchemy.util import OrderedDict

import ckan.model as model
from ckanext.importlib.importer import *
import ckanext.importlib.spreadsheet_importer as spreadsheet_importer

import ckanext.ngds.lib.importer.helper as import_helper

#Need to decide our own Read only keys
readonly_keys = ('id', 'revision_id',
                 'relationships',
                 'license',
                 'ratings_average', 'ratings_count',
                 'ckan_url',
                 'metadata_modified',
                 'metadata_created',
                 'notes_rendered')


def importrecordclient(file_path=None,resource_dir=None):
    #print "Entered Import Record Client:",file_path
    from ckan.lib.navl.dictization_functions import DataError, unflatten, validate
    from ckan.logic import (tuplize_dict,clean_dict,parse_params,flatten_to_string_key)

    from ckanclient import CkanClient
    from ckanext.ngds.lib.importer.loader import ResourceLoader

    testclient = CkanClient(base_location='http://localhost:5000/api', api_key="5364e36d-0bd0-43af-be38-452149466950")
    loader = ResourceLoader(testclient,field_keys_to_find_pkg_by=['name'],resource_dir=resource_dir)
      
    package_import = NGDSPackageImporter(filepath=file_path)

    pkg_dicts = [pkg_dict for pkg_dict in package_import.pkg_dict()]

    for pkg_dict in pkg_dicts:
        #print "Processing Package: ",pkg_dict
        try:
            loader.load_package(clean_dict(unflatten(tuplize_dict(pkg_dict))))
        except Exception , e:
            print "Skipping this record and proceeding with next one....",e 

class SpreadsheetDataRecords(DataRecords):
    '''Takes SpreadsheetData and converts it its titles and
    data records. Handles title rows and filters out rows of rubbish.
    '''
    def __init__(self, spreadsheet_data, essential_title):
        assert isinstance(spreadsheet_data, SpreadsheetData), spreadsheet_data
        self._data = spreadsheet_data
        # find titles row
        self.titles, last_titles_row_index = self.find_titles(essential_title)
        #print "Titles: ",self.titles
        self._first_record_row = self.find_first_record_row(last_titles_row_index + 1)     

    def find_titles(self, essential_title):
        #print "Here essential_title: ",essential_title
        row_index = 0
        titles = []
        essential_title_lower = essential_title.lower()
        #print "Number of rows:",self._data.get_num_rows()
        #print "essential_title:",essential_title
        while True:
            #print "row_index:",row_index
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
        #print "Returning from NGDS records...."
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
        super(NGDSPackageImporter, self).__init__(**kwargs)
        
    # def import_into_package_records(self):
    #     try: 
    #         package_data = CsvData(self.log, filepath=self._filepath,
    #                                buf=self._buf)
    #     except ImportException:
    #         package_data = XlData(self.log, filepath=self._filepath,
    #                               buf=self._buf, sheet_index=0)
    #         if package_data.get_num_sheets() > 1:
    #             package_data = [XlData(self.log, filepath=self._filepath,
    #                               buf=self._buf, sheet_index=i) for i in range(package_data.get_num_sheets())]
    #     self._package_data_records = MultipleSpreadsheetDataRecords(
    #         data_list=package_data,
    #         record_params=self._record_params,
    #         record_class=self._record_class)
        
    # def record_2_package(self, row_dict):
    #     pkg_dict = self.pkg_xl_dict_to_fs_dict(row_dict, self.log)
    #     return pkg_dict

    @classmethod
    def license_2_license_id(self, license_title, logger=None):
        # import is here, as it creates a dependency on ckan, which
        # many importers won't want
        from ckan.model.license import LicenseRegister
        #print "license_title: ",license_title
        licenses = LicenseRegister()
        #print "licenses: ",licenses
        license_obj = licenses.get(license_title)
        #print "license_obj: ",license_obj
        if license_obj:
            return u'%s' % license_obj.id
        else:
            #print "license_title: ",license_title
            #logger('Warning: No license name matches \'%s\'. Ignoring license.' % license_title)
            return u''    


        
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
        #import ckan.forms
        standard_fields = model.Package.get_fields()

        #print "Standar Fields: ", standard_fields

        pkg_fs_dict = OrderedDict()
        for title, cell in pkg_xl_dict.items():
            if cell:
                if title == 'private':
                  print "Private value....",cell
                if title in standard_fields:
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
                        if not pkg_fs_dict.has_key('resources'):
                            pkg_fs_dict['resources'] = []
                        resources = pkg_fs_dict['resources']
                        num_new_resources = 1 + res_index - len(resources)
                        for i in range(num_new_resources):
                            blank_dict = OrderedDict()
                            for blank_field in model.Resource.get_columns():
                                blank_dict[blank_field] = u''
                            pkg_fs_dict['resources'].append(blank_dict)

                        # if field =='upload_file':
                        #     #Upload the file and get the URL of it.
                        #     upload_url=import_helper.upload_file_return_path(file_name=cell,file_path="/home/ngds/work/")
                        #     pkg_fs_dict['resources'][res_index]['url'] = upload_url
                            

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
        pkg_fs_dict['owner_org']='public'            
        return pkg_fs_dict

                
# class MultipleSpreadsheetDataRecords(DataRecords):
#     '''Takes several SpreadsheetData objects and returns records for all
#     of them combined.
#     '''
#     def __init__(self, data_list, record_params, record_class=SpreadsheetDataRecords):
#         self.records_list = []
#         if not isinstance(data_list, (list, tuple)):
#             data_list = [data_list]
#         for data in data_list:
#             self.records_list.append(record_class(data, *record_params))
            
#     @property
#     def records(self):
#         for spreadsheet_records in self.records_list:
#             for spreadsheet_record in spreadsheet_records.records:
#                 yield spreadsheet_record