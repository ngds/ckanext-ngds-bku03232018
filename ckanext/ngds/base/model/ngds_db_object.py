''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

from ckan.model.domain_object import DomainObject

class NgdsDataObject(DomainObject):
    """Base class for NGDS database access classes, adds a "by_id" and "get_all" function to ckan.model.domain_object:DomainObject"""
    @classmethod
    def by_id(cls, pk):
        return cls.Session.query(cls).get(pk) # self.Session defined in ckan.model.domain_object:DomainObject
    
    @classmethod
    def get_all(cls):
        return cls.Session.query(cls).all() # self.Session defined in ckan.model.domain_object:DomainObject
