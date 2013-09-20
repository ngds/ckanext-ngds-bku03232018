from ckan.plugins.toolkit import toolkit


class NgdsCrudController():
    """Base class for NGDS CRUD API controllers. Subclasses must set self.model during __init__"""
    model = None # This must be set during sub-class __init__
    
    def execute(self, data_dict):
        """Inspect the data_dict to determine which CRUD operation to perform"""
        
        process = data_dict.get("process", None) # Get the requested process
        data = data_dict.get("data", None) # Get the request data
        
        if process == "create":
            return self.create(data) # Dispatch to the create function
        elif process == "add":
            return self.add(data)
        elif process == "read":
            if data.get("id", None) == None: # 400 if there is no ID given                
                raise toolkit.ValidationError({}, toolkit._("No ID was given."))
            else:
                return self.read(data) # Dispatch to the read function
        elif process == "update":            
            if data.get("id", None) == None: # 400 if there is no ID given                
                raise toolkit.ValidationError({}, toolkit._("No ID was given."))
            else:
                return self.update(data) # Dispatch to the update function
        elif process == "delete":            
            if data.get("id", None) == None: # 400 if there is no ID given                
                raise toolkit.ValidationError({}, toolkit._("No ID was given."))
            else:
                return self.delete(data) # Dispatch to the delete function
        else: # 400 if the request didn't contain an appropriate process            
            raise toolkit.ValidationError({}, toolkit._("Please supply a 'process' attribute in the POST body. Value can be one of: create, read, update, delete"))
    
    def valid_data(self, data):
        """Check if the data contains valid information to generate a model instance"""
        try: # This is only a valid test if validators are defined for the model class
            self.model(**data) # try to make an instance out of it
            return True # Success, data is valid
        except Exception:             
            return False # fail! data is invalid
            
    # These functions are responsible for CRUD actions
    # ------------------------------------------------        
    def create(self, data):
        """Save a new object to the database"""
        if self.valid_data(data):
            instance = self.model(**data)
            instance.save() # Automatically commits, save() defined by ckan.model.domain_object:DomainObject
            print instance.as_dict()
            return instance.as_dict() # as_dict() defined by ckan.model.domain_object:DomainObject
        else: # 400 if the data is not valid
            raise toolkit.ValidationError({}, toolkit._("Please supply a 'data' attribute containing the appropriate content for a %s instance.") % self.model.__name__)

    def add(self, data):
        """Save a new object to the database"""
        if self.valid_data(data):
            instance = self.model(**data)
            instance.add() # No Commit.
            return instance.as_dict() # as_dict() defined by ckan.model.domain_object:DomainObject
        else: # 400 if the data is not valid
            raise toolkit.ValidationError({}, toolkit._("Please supply a 'data' attribute containing the appropriate content for a %s instance.") % self.model.__name__)
            
    def read(self, data):
        """Read an object from the database"""        
        pk = data.get("id")
        if pk == "all": # If request is for every instance...
            result = [ instance.as_dict() for instance in self.model.get_all() ] # Return a list of each instance as_dict()
            return result
        else: 
            instance = self.model.by_id(pk) # by_id() defined by ckanext.ngds.model.ngds_db_object:NgdsDataObject
            if instance:
                return instance.as_dict() # as_dict() defined by ckan.model.domain_object:DomainObject
            else: # 404 if there is nothing by that ID available
                raise toolkit.ObjectNotFound()
    
    def update(self, data):
        """Update an existing object with new data"""
        pk = data.get("id")
        instance = self.model.by_id(pk) # by_id() defined by ckanext.ngds.model.ngds_db_object:NgdsDataObject
        if instance:
            result = instance.as_dict() # as_dict() defined by ckan.model.domain_object:DomainObject
            keys = result.keys() # Grab the keys from as_dict(). These represent the update-able attributes of the instance
            result.update(data) # generate a dict with updates applied to the existing object
            if self.valid_data(result): # Check that the update is feasible
                for key in keys: # Cycle through the update-able attributes of the instance
                    if key in data.keys(): # If the attribute is defined in the incoming data...
                        setattr(instance, key, data[key]) # Update the attribute of the instance
                instance.save() # Done with the loop, save the instance to update the object
                return instance.as_dict() # Return it
            else: # Update does not produce a valid object, 400
                raise toolkit.ValidationError({}, toolkit._("The content supplied in the 'data' attribute would create an invalid %s instance.") % self.model.__name__)
        else: # ID did not correspond to an existing object, 400
            raise toolkit.ObjectNotFound()
        
    def delete(self, data):
        """Delete an existing object from the database"""
        pk = data.get("id")
        instance = self.model.by_id(pk) # by_id() ckanext.ngds.model.ngds_db_object:NgdsDataObject
        if instance:
            instance.delete() # delete() defined by ckan.model.domain_object:DomainObject
            instance.commit() # commit() defined by ckan.model.domain_object:DomainObject
        else: # ID did not correspond to an existing instance, 400
            raise toolkit.ObjectNotFound()