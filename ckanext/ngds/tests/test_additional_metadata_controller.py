from nose.tools import ok_, eq_
from ckanext.ngds.tests.base import MetadataTestBase

from ckan import model
from ckan.model import Package, Session, meta
from ckanext.ngds.metadata.controllers import additional_metadata

class TestAdditionalMetadata(MetadataTestBase):
    context = {
            "model": model,
            "session": Session,
            "user": "tester",
            "api_version": 2
        }    
     
    def create_rp_record(self):
        import random
        rp_id = random.randint(1, 10000)
        rp_script = "(" + str(rp_id) + ", 'Genhan Chen', 'genhan.chen@azgs.az.gov', 'Arizona Geological Survey', '520-209-4136', '416 W. Congress St. Ste. 100', 'AZ', 'Tucson', '85701')"
        self._create_record('responsible_party', rp_script)
        return rp_id
            
    def test_dispatch(self):
        rp_id = self.create_rp_record() 
                    
        """ Test if dispatch function works for responsible_party table """     
        
        post_data_rp = {
                "model": "ResponsibleParty", 
                "process": "create",
                "data": {
                    "name": "Genhan Chen",
                    "email": "genhan.chen@azgs.az.gov",
                    "organization": "Arizona Geological Survey",
                    "phone": "520-209-4136",
                    "street": "416 W. Congress St. Ste. 100",
                    "city": "Tucson",
                    "state": "AZ",
                    "zip": "85701"
                }
            }
        
        try:
            additional_metadata.dispatch(self.context, post_data_rp)
        except:
            ok_(False, "The dispatch function cannot determine responsible party controller!") 
        
   
        """ Test if dispatch function works for package_additional_metadata table """
             
        post_data_pam = {
                    "model": "AdditionalPackageMetadata", 
                    "process": "create",
                    "data": {
                             "package_id": model.Package.get("test-ngds").id,
                             "author_id": rp_id,
                             "maintainer_id": rp_id,
                             "pub_date": "2013-03-04",
                             "resource_type": "Dataset"
                        }
            }
        
        try:
            additional_metadata.dispatch(self.context, post_data_pam)
        except:
            ok_(False, "The dispatch function cannot determine package additional metadata controller!") 
        
        
        """ Test if dispatch function works for resource_additional_metadata table """
          
        post_data_ram = {
                    "model": "AdditionalResourceMetadata", 
                    "process": "create",
                    "data": {
                             "resource_id": model.Resource.get('test-resource').id,
                             "distributor_id": rp_id
                        }                    
            }
            
        try:
            additional_metadata.dispatch(self.context, post_data_ram)
        except:
            ok_(False, "The dispatch function cannot determine resource additional metadata controller!")
    
        
        """ Test if dispatch function can identify the invalid input model """
        
        from ckan.logic import ValidationError
        post_data_invalid = {
                    "model": "InvalidModel", 
                    "process": "create",
                    "data": {}                    
            }
        
        try:
            additional_metadata.dispatch(self.context, post_data_invalid)
            ok_(False, "The dispatch function cannot identify the invalid model!")
        except ValidationError:
            pass
        else:
            ok_(False, "The dispatch function cannot identify the invalid model!")
                  
    
    def test_class_AdditionalResourceMetadataController(self):
        """ Test if AdditionalResourceMetadataController can find the right model """
        expected_model = self.context["model"].AdditionalResourceMetadata
        model = additional_metadata.AdditionalResourceMetadataController(self.context).model
        
        eq_(model, expected_model, "AdditionalResourceMetadataController cannot find the right model")
        
    def test_class_AdditionalPackageMetadataController(self):
        """ Test if AdditionalPackageMetadataController can find the right model """
        expected_model = self.context["model"].AdditionalPackageMetadata
        model = additional_metadata.AdditionalPackageMetadataController(self.context).model
        
        eq_(model, expected_model, "AdditionalPackageMetadataController cannot find the right model")
        
    def test_class_ResponsiblePartyController(self):
        """ Test if ResponsiblePartyController can find the right model """
        expected_model = self.context["model"].ResponsibleParty
        model = additional_metadata.ResponsiblePartyController(self.context).model
        
        eq_(model, expected_model, "ResponsiblePartyController cannot find the right model")