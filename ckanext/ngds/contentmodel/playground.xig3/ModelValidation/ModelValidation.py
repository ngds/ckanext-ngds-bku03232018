'''
Created on Apr 12, 2013

@author: xig3
'''

import urllib2, sys, simplejson

from ContentModel_Definitions import *
from ContentModel_Utilities   import *

playground = ContentModel_Playground()

def load_schema (schema_uri, version_string):
    global playground
    print "about to start schema reading"
    
    remotefile = urllib2.urlopen("http://schemas.usgin.org/contentmodels.json")
    #remotefile = urllib2.urlopen("file:///home/xig3/workspace/ModelValidation/samples/contentmodels.json")
    result = simplejson.load(remotefile)
    schemaList = [ rec for rec in result if rec['uri'] ==  schema_uri]
    # print schemaList
    
    versions = schemaList[0]['versions']
    version  = [ rec for rec in versions if rec['version'] == version_string]
    # print version
    
    field_info_list = version[0]['field_info']
    print field_info_list
    
    for field_info in field_info_list:
        playground.fieldModelList.append(ContentModel_FieldInfoCell(field_info['optional'], field_info['type'], field_info['name'], field_info['description']))

    print "about to finish schema reading, find " + str(len(playground.fieldModelList)) + " field information"  
# def load_schema (schema_uri, version_string)

def load_csv(csv_filename):
    global playground
    print "about to start CSV reading"
    
    csv_data = ContentModel_CSVData(csv_filename)
    
    try:
        header = csv_data.csv_reader.next()
        playground.dataHeaderList = [x.strip() for x in header]
        
        for row in csv_data.csv_reader:
            new_row = [x.strip() for x in row]
            playground.dataListList.append(new_row)
    except csv.Error as e:
        sys.exit("file %s, line %d: %s" %(csv_filename, csv_data.csv_reader.line_num, e))

    print "about to finish CSV reading"
# def load_csv(csv_filename)

def validate_existence():
    global playground
    print "about to start field existence checking"
    
    # build link between dataHeaderList and fieldInfoList
    # fieldInfo_index = linkToFieldInfoFromHeader[headaer_index]
    linkToFieldInfoFromHeader = []
    for header in playground.dataHeaderList:
        index = [i for i, field in enumerate(playground.fieldModelList) if field.name == header]
        linkToFieldInfoFromHeader.append(index[0])
        
    OptionalFalseIndex = []
    for i in xrange(len(playground.dataHeaderList)):
        if   playground.fieldModelList[linkToFieldInfoFromHeader[i]].optional == False:
            OptionalFalseIndex.append(i)
    print "OptionalFalseIndex:"
    print OptionalFalseIndex
    
    for jd in xrange(len(playground.dataListList)):
        for i in xrange(len(OptionalFalseIndex)):
            data = playground.dataListList[jd][OptionalFalseIndex[i]]
            if (len(data)==0) or (data.isspace()):
                print "cell (%d,%d): %s (field %s) is defined as optional false" %(jd+2, i+1, data, playground.dataHeaderList[OptionalFalseIndex[i]])

    print "about to finish field existence checking"
# def validate_existence()

def validate_numericType():
    global playground
    print "about to start numeric data type checking"
    
    # build link between dataHeaderList and fieldInfoList
    # fieldInfo_index = linkToFieldInfoFromHeader[headaer_index]
    linkToFieldInfoFromHeader = []
    for header in playground.dataHeaderList:
        index = [i for i, field in enumerate(playground.fieldModelList) if field.name == header]
        linkToFieldInfoFromHeader.append(index[0])
    
    IntTypeIndex = []
    DoubleTypeIndex = []
    for i in xrange(len(playground.dataHeaderList)):
        if   playground.fieldModelList[linkToFieldInfoFromHeader[i]].typeString == 'int':
            IntTypeIndex.append(i)
        elif playground.fieldModelList[linkToFieldInfoFromHeader[i]].typeString == 'double':
            DoubleTypeIndex.append(i)
    print "IntTypeIndex:"
    print IntTypeIndex
    print "DoubleTypeIndex:"
    print DoubleTypeIndex
    
    for jd in xrange(len(playground.dataListList)):
        # check the int type
        for i in xrange(len(IntTypeIndex)):
            data = playground.dataListList[jd][IntTypeIndex[i]]
            if isInteger(data) == False:
                print "cell (%d,%d): %s (field %s) is expected to be an Integer" %(jd+2, i+1, data, playground.dataHeaderList[IntTypeIndex[i]])
                   
        # check the double type
        for i in xrange(len(DoubleTypeIndex)):
                data = playground.dataListList[jd][DoubleTypeIndex[i]]
                if isNumber(data) == False:
                    print "cell (%d,%d): %s (field %s) is expected to be a  Numeric" %(jd+2, i+1, data, playground.dataHeaderList[DoubleTypeIndex[i]])
    
# def validate_numericType()

def main(csv_filename, schema_uri, version_string):
    global playground
    print "action is about to start"
    
    load_schema(schema_uri, version_string)
    load_csv(csv_filename)
    playground.display()
    
    print "start checking existence"
    validate_existence()
    validate_numericType()
    playground.report()
    
# def main(csv_filename, schema_uri, version_string)

if __name__ == '__main__':
    csv_filename = sys.argv[1]
    schema_uri   = sys.argv[2]
    version_string = sys.argv[3]
    
    main(csv_filename, schema_uri, version_string)
    print "done"
