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
__author__ = 'kaffeine'
import ckan.model as model


class Customize(object):
    def customize(self):
        from pylons import config

        group_name = config.get('ngds.default_group_name', 'public')
        check = model.group.Group.by_name(group_name)
        print check
        if not check:
            # Then create
            model.repo.new_revision()
            new_group = model.group.Group(group_name)
            new_group.is_organization = True
            model.Session.add(new_group)
            model.repo.commit_and_remove()
