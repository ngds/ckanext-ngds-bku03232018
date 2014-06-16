""" NGDS_HEADER_BEGIN

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey

Please refer the the README.txt file in the base directory of the NGDS project:
https://github.com/ngds/ckanext-ngds/blob/master/README.txt

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero
General Public License as published by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.  https://github.com/ngds/ckanext-ngds
ngds/blob/master/LICENSE.md or
http://www.gnu.org/licenses/agpl.html

NGDS_HEADER_END """

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
