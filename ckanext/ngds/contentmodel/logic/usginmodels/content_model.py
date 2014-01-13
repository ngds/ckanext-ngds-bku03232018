from datetime import datetime
from dateutil import parser as date_parser

from model_version import ModelVersion
from exceptions import *

class ContentModel():

    title = ""
    label = ""
    description = ""
    uri = ""
    date_updated = datetime(1900, 1, 1)
    versions = []

    def __init__(self, model_dict):
        self.title = model_dict.get("title", "")
        self.label = model_dict.get("label", "")
        self.description = model_dict.get("description", "")
        self.uri = model_dict.get("uri", "")

        self.date_updated = date_parser.parse(model_dict.get("date_updated", self.date_updated.isoformat()))
        self.versions = [ModelVersion(v) for v in model_dict.get("versions", [])]

    def latest_version(self):
        """
        Return the latest version
        """
        sorted_versions = sorted(self.versions, key=lambda v: v.date_created)
        if len(sorted_versions) == 0:
            return None

        return sorted_versions[-1]

    def is_version_valid(self, version_id_or_uri):
        """
        Might pass in "1.1" or "http://schemas.usgin.org/uri-gin/ngds/dataschema/activefaults/1.1"
        """
        uri_components = version_id_or_uri.split("/")
        version = uri_components.pop() if len(uri_components) > 1 else version_id_or_uri
        return version in [v.version for v in self.versions]

    def validate_file(self, csv_file):
        """
        Validate the file against the latest version of the model
        """
        latest = self.latest_version()
        latest.validate_file(csv_file)

    def get_version(self, version_id_or_uri):
        if not self.is_version_valid(version_id_or_uri):
            raise InvalidUri(version_id_or_uri)

