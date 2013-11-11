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
            
    def test_dispatch(self):
                    
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
                    "zip": "85701",
                    "country": "US"
                }
            }
        
        try:
            additional_metadata.dispatch(self.context, post_data_rp)
        except:
            ok_(False, "The dispatch function cannot determine responsible party controller!") 
        
    def test_class_ResponsiblePartyController(self):
        """ Test if ResponsiblePartyController can find the right model """
        expected_model = self.context["model"].ResponsibleParty
        model = additional_metadata.ResponsiblePartyController(self.context).model
        
        eq_(model, expected_model, "ResponsiblePartyController cannot find the right model")