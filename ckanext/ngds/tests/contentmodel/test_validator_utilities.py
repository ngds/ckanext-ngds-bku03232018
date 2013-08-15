from nose.tools import *

from ckanext.ngds.contentmodel.logic.action import *

import urllib2, sys, simplejson
import csv

# Use this method to initialize the database
def setUp(self):
    print ">>>>>>>>> Test Steup >>>>>>>>"
    assert True


# Use this method to reset the database
def teardown(self):
    print ">>>>>>>>>> Test Teardown >>>>>>>"
    assert True
    
def support_contentmodel_get(data_dict):
    '''Returns the information about a certain content model.
    
    **Parameters:**
    :param cm_uri: uri of the content model.
    :type cm_uri: string

    :param cm_version: version of the content model.
    :type cm_version: string
    '''
#    remotefile = urllib2.urlopen("http://schemas.usgin.org/contentmodels.json")
#    ckanext.ngds.contentmodel.model.contentmodels.contentmodels = simplejson.load(remotefile)
    
    json_file = open("./testdata/contentmodels.json")
    ckanext.ngds.contentmodel.model.contentmodels.contentmodels = simplejson.load(json_file)
    json_file.close()
    
    cm_uri = data_dict['cm_uri']
    cm_version= data_dict['cm_version']
    
    schema= [ rec for rec in ckanext.ngds.contentmodel.model.contentmodels.contentmodels
              if rec['uri'] == cm_uri ]
    
    # schema is a list with a single entry
    schema_versions= schema[0]['versions']
    
    version= [ rec for rec in schema_versions if rec['version'] == cm_version]
    # version is again a list with a single entry
    return version[0]

def support_filter_valid_model(user_schema):
    fieldModelList = []
    field_info_list = user_schema['field_info']
    for field_info in field_info_list:
        if ((field_info['name'] is None) and ((len(field_info['type'])==0) or (field_info['type'].isspace()))):
            print "found a undefined field: " + str(field_info)  
            continue
        else: 
            fieldModelList.append(ContentModel_FieldInfoCell(field_info['optional'], field_info['type'], field_info['name'], field_info['description']))
    print fieldModelList
    print "finish schema reading, find " + str(len(fieldModelList)) + " field information"  
    return fieldModelList

def support_CSV_loader(csv_filename):
    validation_msg = []
    dataHeaderList = []
    dataListList = []
    if len(validation_msg) == 0:
        try:
            print "csv_filename: %s" %(csv_filename)
            csv_reader = csv.reader(open(csv_filename, "rbU"))
            header = csv_reader.next()
            dataHeaderList = [x.strip() for x in header]
            
            for row in csv_reader:
                new_row = [x.strip() for x in row]
                dataListList.append(new_row)
        except csv.Error as e:
            msg = "csv.Error file %s, line %d: %s" %(csv_filename, csv_reader.line_num, e)
            validation_msg.append({'row':0, 'col':0, 'errorTYpe': 'systemError', 'message':msg})
        except IOError as e:
            msg = "IOError file %s, %s" %(csv_filename, e)
            validation_msg.append({'row':0, 'col':0, 'errorTYpe': 'systemError', 'message':msg})
    print "load %d headers" %(len(dataHeaderList))
    print "load %d row records" %(len(dataListList))
    print "about to finish CSV reading"
    return {'validation_msg':validation_msg, 'dataHeaderList':dataHeaderList, 'dataListList':dataListList}

def test_data_has_extra_column_compare_to_model():
    csv_file_path = "../../../../sample-data/ca-boreholetemperature.csv"
    data_dict = {"cm_uri":"http://schemas.usgin.org/uri-gin/ngds/dataschema/Metadata/", "cm_version":"1.3.5"}
    
    user_schema = support_contentmodel_get(data_dict)
    print(user_schema)
    
    fieldModelList = support_filter_valid_model(user_schema)
    print(fieldModelList)
    
    csv_data = support_CSV_loader(csv_file_path)
    assert_equals(csv_data['validation_msg'],[])
    
    validate_header_messages = validate_header(fieldModelList, csv_data['dataHeaderList'], csv_data['dataListList'])
    print validate_header_messages
    assert len(validate_header_messages) > 0

def test_data_miss_must_have_column_compare_to_model():
    csv_file_path = "./testdata/PowerPlantFacility_missingColumn.csv"
    data_dict = {"cm_uri":"http://schemas.usgin.org/uri-gin/ngds/dataschema/PowerPlantFacility/", "cm_version":"0.2"}
    
    user_schema = support_contentmodel_get(data_dict)
    print(user_schema)
    
    fieldModelList = support_filter_valid_model(user_schema)
    print(fieldModelList)
    
    csv_data = support_CSV_loader(csv_file_path)
    assert_equals(csv_data['validation_msg'],[])
    
    validate_header_messages = validate_detectMissingColumn(fieldModelList, csv_data['dataHeaderList'])
    print validate_header_messages
    assert len(validate_header_messages) > 0

def test_data_empty_cell():
    csv_file_path = "./testdata/PowerPlantFacility_missingValue.csv"
    data_dict = {"cm_uri":"http://schemas.usgin.org/uri-gin/ngds/dataschema/PowerPlantFacility/", "cm_version":"0.2"}
    
    user_schema = support_contentmodel_get(data_dict)
    print(user_schema)
    
    fieldModelList = support_filter_valid_model(user_schema)
    print(fieldModelList)
    
    csv_data = support_CSV_loader(csv_file_path)
    assert_equals(csv_data['validation_msg'],[])
    
    validation_existence_messages = validate_existence(fieldModelList, csv_data['dataHeaderList'], csv_data['dataListList'])
    print validation_existence_messages
    assert len(validation_existence_messages) > 0
    
def test_data_Numeric1():
    assert_equals(isNumber("-1.0"), True)
    assert_equals(isNumber("-1"  ), True)
    assert_equals(isNumber("-0"  ), True)
    assert_equals(isNumber("1.0" ), True)
    assert_equals(isNumber("2"   ), True)
    assert_equals(isNumber(".99" ), True)
    assert_equals(isNumber(" "   ), False)
    assert_equals(isNumber("s"   ), False)
    
def test_data_Numeric2():
    assert_equals(isInteger("-1.0"), False)
    assert_equals(isInteger("-1"  ), True)
    assert_equals(isInteger("-0"  ), True)
    assert_equals(isInteger("1.0" ), False)
    assert_equals(isInteger("2"   ), True)
    assert_equals(isInteger(".99" ), False)
    assert_equals(isInteger(" "   ), False)
    assert_equals(isInteger("s"   ), False)
    
def test_data_Number1():
    csv_file_path = "./testdata/PowerPlantFacility_Number.csv"
    data_dict = {"cm_uri":"http://schemas.usgin.org/uri-gin/ngds/dataschema/PowerPlantFacility/", "cm_version":"0.2"}
    
    user_schema = support_contentmodel_get(data_dict)
    print(user_schema)
    
    fieldModelList = support_filter_valid_model(user_schema)
    print(fieldModelList)
    
    csv_data = support_CSV_loader(csv_file_path)
    assert_equals(csv_data['validation_msg'],[])
    
    validation_numericType_messages = validate_numericType(fieldModelList, csv_data['dataHeaderList'], csv_data['dataListList'])
    print validation_numericType_messages
    assert len(validation_numericType_messages) > 0

def test_data_Number2():
    csv_file_path = "./testdata/PowerPlantFacility_NumberOK.csv"
    data_dict = {"cm_uri":"http://schemas.usgin.org/uri-gin/ngds/dataschema/PowerPlantFacility/", "cm_version":"0.2"}
    
    user_schema = support_contentmodel_get(data_dict)
    print(user_schema)
    
    fieldModelList = support_filter_valid_model(user_schema)
    print(fieldModelList)
    
    csv_data = support_CSV_loader(csv_file_path)
    assert_equals(csv_data['validation_msg'],[])
    
    validation_numericType_messages = validate_numericType(fieldModelList, csv_data['dataHeaderList'], csv_data['dataListList'])
    print validation_numericType_messages
    assert len(validation_numericType_messages) == 0
    
if __name__ == '__main__':
    test_data_has_extra_column_compare_to_model()
    test_data_miss_must_have_column_compare_to_model()
    test_data_empty_cell()
    test_data_Numeric1()
    test_data_Numeric2()
    test_data_Number1()
    test_data_Number2()
    print "done"
