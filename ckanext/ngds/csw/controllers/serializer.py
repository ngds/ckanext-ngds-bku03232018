from ckan.plugins import toolkit
from ckan.lib.base import BaseController
import json

class PackageSerializer(BaseController):
    """
    Controls responses to GET requests for serialized metadata
    """

    def dispatch(self, *args, **kwargs):
        format = kwargs.get("format", "")

        if format == "xml":
            kwargs.get("pylons").response.content_type = "text/xml"
            return self.xml(kwargs.get("package_id", ""))

        elif format == "json":
            kwargs.get("pylons").response.content_type = "application/json"
            return self.json(kwargs.get("package_id", ""))

        else:
            return "Format was not properly specified"

    def xml(self, package_id):
        return toolkit.get_action("iso_metadata")(None, {"id": package_id})

    def json(self, package_id):
        result = toolkit.get_action("package_show")(None, {"id": package_id})
        return json.dumps(result)