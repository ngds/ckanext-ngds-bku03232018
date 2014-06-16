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

import os

from nose.tools import *

import ckanext.ngds.importer.validator as ngdsvalidator


# Use this method to initialize the database
def setUp(self):
    print ">>>>>>>>> Test Steup >>>>>>>>"
    assert True


# Use this method to reset the database
def teardown(self):
    print ">>>>>>>>>> Test Teardown >>>>>>>"
    assert True


def test_find_column_pos1():
    xl_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata", "test_find_pos.xls"))
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>xl_file_path:", xl_file_path
    validator = ngdsvalidator.NGDSValidator(filepath=xl_file_path, resource_path=None, resource_list=None)

    validator.find_column_pos()

    #compare the expected column positions.
    print "self.mandatory_keys_pos: ", validator.mandatory_keys_pos
    print 'self.mandatory_keys_pos: %s date_field_pos: %s upload_file_pos: %s' % (validator.mandatory_keys_pos, validator. date_field_pos, validator.upload_file_pos)
    assert_equals(validator.mandatory_keys_pos, [(0, u'name'), (1, u'title')])
    assert_equals(validator.date_field_pos, [])
    assert_equals(validator.upload_file_pos, [(13, u'resource-0-upload_file')])

def test_find_column_pos2():
    xl_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata", "test_find_pos1.xls"))
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>xl_file_path:", xl_file_path
    validator = ngdsvalidator.NGDSValidator(filepath=xl_file_path, resource_path=None, resource_list=None)

    validator.find_column_pos()

    print "self.mandatory_keys_pos: ", validator.mandatory_keys_pos
    print 'self.mandatory_keys_pos: %s date_field_pos: %s upload_file_pos: %s' % (validator.mandatory_keys_pos, validator.date_field_pos, validator.upload_file_pos)
    assert_equals(validator.mandatory_keys_pos, [(0, u'name'), (1, u'title')])
    assert_equals(validator.date_field_pos, [(8, u'publication_date')])
    assert_equals(validator.upload_file_pos, [(14, u'resource-0-upload_file')])

@raises(Exception)
def test_without_title_row():

    xl_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata", "without_title_row.xls"))
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>xl_file_path:", xl_file_path
    validator = ngdsvalidator.NGDSValidator(filepath=xl_file_path, resource_path=None, resource_list=None)

    validator.find_column_pos()

    print "self.mandatory_keys_pos: ",validator.mandatory_keys_pos
    print 'self.mandatory_keys_pos: %s date_field_pos: %s upload_file_pos: %s' % (validator.mandatory_keys_pos,validator.date_field_pos,validator.upload_file_pos)
    assert_equals(validator.mandatory_keys_pos,[(0,u'name'),(1,u'title')])
    assert_equals(validator.date_field_pos,[(8, u'publication_date')])
    assert_equals(validator.upload_file_pos,[(14, u'resource-0-upload_file')])        

@raises(Exception)
def test_without_mandatory_fields():
    xl_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata", "without_mandatory.xls"))
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>xl_file_path:", xl_file_path
    validator = ngdsvalidator.NGDSValidator(filepath=xl_file_path, resource_path=None, resource_list=None)

    validator.find_column_pos()
    validator._validate_mandatory_field()

@raises(Exception)
def test_invalid_date_fields():
    xl_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata", "invalid_date_fields.xls"))
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>xl_file_path:", xl_file_path
    validator = ngdsvalidator.NGDSValidator(filepath=xl_file_path, resource_path=None, resource_list=None)

    validator.find_column_pos()
    try:
        validator._validate_date_field()    
    except Exception, e:
        print "exception: ",e
        assert False

def test_valid_file():
    xl_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata", "test_find_pos.xls"))
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>xl_file_path:", xl_file_path
    validator = ngdsvalidator.NGDSValidator(filepath=xl_file_path, resource_path=None, resource_list=None)

    validationResponse = validator.validate()

    assert validationResponse
