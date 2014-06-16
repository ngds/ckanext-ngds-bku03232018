""" NGDS_HEADER_BEGIN

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey

Please refer the the README.txt file in the base directory of the NGDS project:
https://github.com/ngds/ckanext-ngds/blob/master/README.txt

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero
General Public License as published by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.  https://github.com/ngds/ckanext-ngds
ngds/blob/master/LICENSE.md or
http://www.gnu.org/licenses/agpl.html

NGDS_HEADER_END """

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
