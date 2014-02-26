__author__ = 'adrian'

from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService
from ckanext.ngds.geoserver.model.Geoserver import Geoserver

class EnforceUSGIN():

    def __init__(self):
        self.geoserver = Geoserver.from_ckan_config()

    def get_all_stores(self):
        store_objects = self.geoserver.get_stores()
        return [store for store in store_objects]

    def get_all_workspaces(self):
        workspace_objects = self.geoserver.get_workspaces()
        return [space for space in workspace_objects]

    def get_all_resources(self):
        resource_objects = self.geoserver.get_resources()
        return [resource for resource in resource_objects]

    def get_workspace_resources(self, workspace='NGDS'):
        this_workspace = workspace.lower()
        resources = self.get_all_resources()
        try:
            workspace_resources = []
            for resource in resources:
                that_workspace = resource.workspace.name.lower()
                if that_workspace == this_workspace:
                    workspace_resources.append(resource)
            return workspace_resources
        except:
            return ['ERROR: EITHER WORKSPACE OR RESOURCES NOT FOUND']

a = EnforceUSGIN()