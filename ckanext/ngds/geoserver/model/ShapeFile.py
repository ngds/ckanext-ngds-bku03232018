from ckanext.ngds.geoserver.model.Data import Data
from ckan.plugins import toolkit

class Shapefile(Data):
    resource = None

    def __init__(self, resource_id):
        self.resource = toolkit.get_action("resource_show")(None, {"id": resource_id})
        self.zip_file = ""

        
        pass

    def unzip(self):
        pass

    def reproject(self):
        pass

    def validate(self):
        pass

	def publish(self):
		pass

	def unpublish(self):
		pass