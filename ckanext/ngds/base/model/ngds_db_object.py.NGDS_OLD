from ckan.model.domain_object import DomainObject

class NgdsDataObject(DomainObject):
    """Base class for NGDS database access classes, adds a "by_id" and "get_all" function to ckan.model.domain_object:DomainObject"""
    @classmethod
    def by_id(cls, pk):
        return cls.Session.query(cls).get(pk) # self.Session defined in ckan.model.domain_object:DomainObject
    
    @classmethod
    def get_all(cls):
        return cls.Session.query(cls).all() # self.Session defined in ckan.model.domain_object:DomainObject