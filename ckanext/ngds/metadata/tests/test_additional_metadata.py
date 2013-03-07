from nose.tools import ok_, eq_, raises
import requests, json

from ckanext.ngds.metadata.tests.base import MetadataTestBase

from sqlalchemy import create_engine

from ckan import model
from ckan.model import Package, Session, meta
from ckanext.ngds.metadata.controllers import additional_metadata
from datetime import datetime

class TestDispatch(MetadataTestBase):

    '''  
    def responsibleparty_create(self):

        post_data = {"model": "ResponsibleParty", "process": "create"}
        post_data.update({"data": self.base_data})
        
        res = requests.post("http://%s/api/action/additional_metadata" % self.host,
                          data=json.dumps(post_data),
                          headers={'Content-Type': 'application/json'})
        response = json.loads(res.content)

        ok_(response["success"])
        
        if response["success"] : 
            result = response["result"]
            self._delete_record("responsible_party", result["id"])
    '''
            
    def test_dispatch(self):       
        '''
        Test if dispatch function works for responsible_party table 
        '''
        
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
        
        context = {
                "model": model,
                "session": Session,
                "user": "tester",
                "api_version": 2
            }
        
        try:
            res = additional_metadata.dispatch(context, post_data_rp)
        finally:
            print "The dispatch function cannot determine responsible party controller!" 
        
