''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

'''
Created on Apr 12, 2013

@author: xig3
'''

class ContentModel_FieldInfoCell(object):
    '''
    field information cell
    '''

    def __init__(self, optional=None, typeString=None, name=None, description=None):
        self.optional    = optional
        self.typeString  = typeString
        self.name        = name
        self.description = description
        
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        #return str(self.name)
        #return str(self.typeString) 
        return "{name:" + str(self.name) + ", type:" + str(self.typeString) + ", opt:" + str(self.optional) + "}"

# class ContentModel_FieldInfoCell(object)


import csv

class ContentModel_CSVData(object):
    '''
    user input CSV file
    '''

    def __init__(self, CSV_filename):
        self.csv_reader = csv.reader(open(CSV_filename, "rb"))

# class ContentModel_CSVData(object)


class ContentModel_Playground(object):
    '''
    where data gets stored
    '''

    def __init__(self):
        self.fieldModelList = []
        self.dataHeaderList = []
        self.dataListList   = []

    def display(self):
        print "ContentModel_Playground"
        print self.fieldModelList
        print self.dataHeaderList
        for rowData in self.dataListList:
            print rowData
            
    def report(self):
        pass
            
# class ContentModel_Playground(object)
