import ckanext.ngds.lib.importer.helper as import_helper
import ckanext.ngds.lib.importer.importer as ngds_importer
import ckanext.importlib.spreadsheet_importer as spreadsheet_importer

referenced_keys = ('category','status','topic','protocol')

date_keys = ('publication_date')
mandatory_keys = ('name','title')

class BasicLogger:
    def __init__(self):
        self.log = []

class NGDSValidator(object):

    def __init__(self,filepath,resource_path=None,resource_list=None):
        """
        filepath - path of Excel to be validated
        resource_path - Path of extracted resources 
        resource_list - list of resources uploaded along with xls data file.
        """
        self._filepath = filepath
        self._resource_path = resource_path
        self._resource_list = resource_list
        self.log = BasicLogger()

    def load_XL(self):
        """
        Loads the xls data into memory for further processing.
        Finds the title row index and first data record index using SpreadsheetDataRecords
        """
        log = BasicLogger()       
        self.xl_data = spreadsheet_importer.XlData(log, filepath=self._filepath,
            buf=None, sheet_index=0)
        spreadsheetData = ngds_importer.SpreadsheetDataRecords(self.xl_data,'Title')

        self.title_row_index = spreadsheetData.last_titles_row_index
        self.first_record_index = spreadsheetData._first_record_row

    def validate(self):
        """
        This method will validate the data file and the resources.If the validation is 
        successfull then returns Status as "VALID" otherwise throws the exception with error message.
        """ 
        self.load_XL()
        self.find_column_pos()

        self._validate_mandatory_field()
        self._validate_date_field()
        #if self._resource_list:
        self._validate_resources_tobe_uploaded()

        return True

    def _validate_date_field(self):
        """
        Validates the fields of type "Date". Iterates through list of date columns and 
        validates the value of each cell to check whether it is valid date format.  
        If one of the fields are not valid date format then throws exception.
        """
        print "validating date fields."
        import datetime
        import xlrd

        for col_index,title in self.date_field_pos:
            date_column = self.xl_data.sheet.col_values(col_index,start_rowx=self.first_record_index)

            try:
                for cell in date_column:
                #for row_index in range(self.first_record_index,self.xl_data.get_num_rows()):
                    #cell = self.xl_data.sheet.cell(row_index, col_index)
                    #if cell and cell.value:
                    if cell:
                        date_tuple = xlrd.xldate_as_tuple(cell, self.xl_data._book.datemode)
                        value = datetime.date(*date_tuple[:3])  
            except Exception , e:
                raise Exception ("Invalid date value: '%s' for the field: %s" % cell,title)

    def _validate_mandatory_field(self):

        """
        Iterates through the list of mandatory columns and if any of the records missing 
        the value then throws exception.
        """
        print "validating mandatory fields."
        for col_index,title in self.mandatory_keys_pos:
            mandatory_column = self.xl_data.sheet.col_values(col_index,
                start_rowx=self.first_record_index)
            if not all(cell for cell in mandatory_column):
                raise Exception("Mandatory field '%s' can't be empty." % title)

    def _validate_resources_tobe_uploaded(self):

        """
        Iterates through each resource file upload fields and check whether the uploaded
        resources are referenced against the package. If not throws an exception.
        """

        print "validating the resources to be uploaded."

        upload_field_list = []
        for col_index,title in self.upload_file_pos:
            upload_field_list.extend(filter(bool,self.xl_data.sheet.col_values(col_index,
                start_rowx=self.first_record_index)))

        upload_field_list = list(set(upload_field_list))

        if self._resource_list:
            for resource in self._resource_list:
                if resource not in upload_field_list:
                    raise Exception("Uploaded resource %s is not referenced against any dataset."%resource)
                    
            if len(upload_field_list) > len(self._resource_list):
                raise Exception("Referenced resources are not uploaded.")                    

        else:
            if len(upload_field_list) > 0 :
                raise Exception("Referenced resources are not uploaded.")
        
    def find_column_pos(self):
        """
        Finds the columns positions to be validated as part of structure validation.
        This method iterates through title fields and compare them with the different to be 
        validated fields and group the positions of the columns.
        """
        import re
        
        self.date_field_pos = []
        self.upload_file_pos = []
        self.mandatory_keys_pos = []

        for col_index in range(self.xl_data.sheet.ncols):
        
            title = self.xl_data.sheet.cell(self.title_row_index, col_index).value
        
            if title in mandatory_keys:
                self.mandatory_keys_pos.append((col_index,title))
        
            if title in date_keys:
                self.date_field_pos.append((col_index,title))
            elif title.find('upload_file'):

                match = re.match('resource-(\d+)-upload_file', title)
                if match:
                    self.upload_file_pos.append((col_index,title))

        #print "mandatory_keys_pos Field positions:",self.mandatory_keys_pos
        #print "date Field positions:",self.date_field_pos
        #print "Upload file Field positions:",self.upload_file_pos