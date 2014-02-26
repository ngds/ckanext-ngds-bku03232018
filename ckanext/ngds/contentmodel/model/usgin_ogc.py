__author__ = 'adrian'

from ckanext.ngds.geoserver.model.Geoserver import Geoserver
from ckan.plugins import toolkit

class EnforceUSGIN(object):

    def __init__(self, data_dict):
        self.geoserver = Geoserver.from_ckan_config()
        self.resource_id = data_dict.get("resource_id")
        self.file_resource = toolkit.get_action("resource_show")(None, {"id": self.resource_id})

    def check_tier_three(self):
        res = self.file_resource
        try:
            return {
                "tier_3": True,
                "content_model": {
                    "uri": res.content_model_uri,
                    "version_uri": res.content_model_version,
                    "layer": res.content_model_layer
                }
            }
        except:
            return {
                "tier_3": False
            }

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

    def check_for_existing_resource(self, resource_id, workspace='NGDS'):
        return