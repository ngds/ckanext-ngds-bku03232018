from nose.tools import ok_, eq_
from ckanext.ngds.tests.base import MetadataTestBase

from ckan import model
from ckan.model import Package, Session, meta
from ckanext.ngds.harvest.controllers import ngds_harvest

class TestNgdsHarvest(MetadataTestBase):
    context = {
            "model": model,
            "session": Session,
            "user": "tester",
            "api_version": 2
        }    
     
    def create_hn_record(self, admin_id):
        import random
        hn_id = random.randint(1, 10000)
        hn_script = "(" + str(hn_id) + ", 'http://azgs.az.gov', '2', 'test', '" + str(admin_id) + "')"
        self._create_record('harvest_node', hn_script)
        return hn_id
    
    def create_rp_record(self):
        import random
        rp_id = random.randint(1, 10000)
        rp_script = "(" + str(rp_id) + ", 'Genhan Chen', 'genhan.chen@azgs.az.gov', 'Arizona Geological Survey', '520-209-4136', '416 W. Congress St. Ste. 100', 'AZ', 'Tucson', '85701', 'US')"
        self._create_record('responsible_party', rp_script)
        return rp_id
           
    def test_dispatch(self):
        rp_id = self.create_rp_record() 
        hn_id = self.create_hn_record(rp_id) 
                    
        """ Test if dispatch function works for harvest_node table """           
        post_data_hn = {
                    "model": "HarvestNode", 
                    "process": "create",
                    "data": {
                             "url": "http://azgs.az.gov",
                             "frequency": "2",
                             "title": "test",
                             "node_admin_id": rp_id
                        }            
            }
        
        try:
            ngds_harvest.dispatch(self.context, post_data_hn)
        except:
            ok_(False, "The dispatch function cannot determine harvest node controller!") 
        
   
        """ Test if dispatch function works for harvested_record table """            
        post_data_hr = {
                    "model": "HarvestedRecord", 
                    "process": "create",
                    "data": {
                             "package_id": model.Package.get("test-ngds").id,
                             "harvest_node_id": hn_id,
                             "harvested_xml": "Test xml document"
                        }  
            }
        
        try:
            ngds_harvest.dispatch(self.context, post_data_hr)
        except:
            ok_(False, "The dispatch function cannot determine harvested record controller!") 
                  
    
    def test_class_HarvestNodeController(self):
        """ Test if HarvestNodeController can find the right model """
        expected_model = self.context["model"].HarvestNode
        model = ngds_harvest.HarvestNodeController(self.context).model
        
        eq_(model, expected_model, "HarvestNodeController cannot find the right model")
        
    def test_class_HarvestedRecordController(self):
        """ Test if HarvestedRecordController can find the right model """
        expected_model = self.context["model"].HarvestedRecord
        model = ngds_harvest.HarvestedRecordController(self.context).model
        
        eq_(model, expected_model, "HarvestedRecordController cannot find the right model")