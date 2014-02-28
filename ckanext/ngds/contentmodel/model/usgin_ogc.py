__author__ = 'adrian'

from ckanext.ngds.geoserver.model.Geoserver import Geoserver
import ckanext.ngds.geoserver.logic.action as action
from ckan.plugins import toolkit
import usginmodels

class EnforceUSGIN(object):

    def __init__(self, context, data_dict):
        self.geoserver = Geoserver.from_ckan_config()
        self.resource_id = data_dict.get("resource_id")
        self.file_resource = toolkit.get_action("resource_show")(None, {"id": self.resource_id})
        self.context = context

    def check_tier_three(self):
        res = self.file_resource
        try:
            return {
                "tier_3": True,
                "content_model": {
                    "uri": res["content_model_uri"],
                    "version_uri": res["content_model_version"],
                    "layer": res["content_model_layer"]
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
            return ["ERROR: Either workspace or resources not found"]

    def create_usgin_workspace(self):
        data = self.check_tier_three()
        if data["tier_3"]:
            version_uri = data["content_model"]["version_uri"]
            layers = usginmodels.get_version(version_uri).layers
            name = usginmodels.get_service_name(version_uri)
            if name == "Invalid":
                return "ERROR: Invalid content model version"
            usgin_workspace = self.geoserver.get_workspace(name)
            if usgin_workspace is None:
                usgin_workspace = self.geoserver.create_workspace(name, version_uri)
            elif usgin_workspace and len(layers) == 1:
                usgin_workspace = "ERROR: Workspace already exists in geoserver"
            elif usgin_workspace and len(layers) > 1:
                usgin_workspace = "MultilayerContentModel"
            else:
                usgin_workspace = "EmptyWorkspace"
            return usgin_workspace
        else:
            return "ERROR: Data is not tier three"

    def create_usgin_layer(self, data_dict):
        data = self.check_tier_three()
        if data["tier_3"]:
            data_dict["layer_name"] = data["content_model"]["layer"]
            data_dict["gs_layer_name"] = data["content_model"]["layer"]
            action.publish(self.context, data_dict)
        else:
            return "ERROR: Data is not tier three"