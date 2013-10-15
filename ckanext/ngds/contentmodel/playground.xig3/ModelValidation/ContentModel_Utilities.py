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

def isNumber(s):
    """
    Checking if a String is a Number
    """
    try:
        float(s)
        return True
    except ValueError:
        pass
    
    return False
# def isNumber(s)

def isInteger(s):
    """
    Checking if a String is an Integer
    """
    try:
        int(s)
        return True
    except ValueError:
        pass
    
    return False
# def isInteger(s)
