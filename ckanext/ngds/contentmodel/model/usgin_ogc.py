__author__ = 'adrian'

from ckanext.ngds.geoserver.model.Geoserver import Geoserver
import ckanext.ngds.geoserver.logic.action as action
from ckan.plugins import toolkit
import usginmodels

class EnforceUSGIN(object):

    def __init__(self, context, data_dict, model_config=None):
        self.geoserver = Geoserver.from_ckan_config()
        self.resource_id = data_dict.get("resource_id")
        self.file_resource = toolkit.get_action("resource_show")(None, {"id": self.resource_id})
        self.context = context
        self.data_dict = data_dict

        if self.model_config is None:
            res = self.file_resource
            try:
                self.model_config = {
                    "uri": res["content_model_uri"],
                    "version_uri": res["content_model_version"],
                    "model_layer": res["content_model_layer"],

                }
                version_uri = self.model_config["version_uri"]
                layers = usginmodels.get_version(version_uri).layers
                name = usginmodels.get_service_name(version_uri)
                if name == "Invalid":
                    return "ERROR: Invalid content model version"
                else:
                    self.model_config["service_name"] = name
                    self.model_config["layers"] = layers
                return self.model_config
            except Exception:
                return Exception


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
            return "ERROR: Either workspace or resources not found"

    def create_usgin_workspace(self):
        this_name = self.model_config["service_name"]
        this_version = self.model_config["version_uri"]
        these_layers = self.model_config["layers"]
        usgin_workspace = self.geoserver.get_workspace(this_name)
        if usgin_workspace is None:
            usgin_workspace = self.geoserver.create_workspace(this_name, this_version)
        elif usgin_workspace and len(these_layers) == 1:
            usgin_workspace = "ERROR: Workspace already exists in Geoserver"
        else:
            return usgin_workspace
        return usgin_workspace

    def create_usgin_layer(self):
        this_store = "datastore"
        this_name = self.model_config["service_name"]
        this_version = self.model_config["version_uri"]
        this_geoserver = self.geoserver.get_datastore(this_name, this_version, this_store)
        self.data_dict["layer_name"] = self.model_config["model_layer"]
        self.data_dict["gs_lyr_name"] = self.model_config["model_layer"]
        self.data_dict["geoserver_instance"] = this_geoserver
        action.publish(self.context, self.data_dict)