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

import ckan.logic as logic


class AbstractFileProcessor(object):
    def __init__(self, file_to_process, content_model, content_model_version, resource_id):
        self.file = file_to_process
        self.resource_id = resource_id
        self.cm = content_model
        self.cmv = content_model_version

    def get_processes(self):
        return self.declare_processes()

    def declare_processes(self):
        pass

    def run_processes(self):
        ps = self.get_processes()

        result_collector = {

        }

        try:
            for process in ps:
                pfunc = process['func']
                metadata_field = process['metadata_field']
                output = pfunc(self.get_file())
                result_collector[metadata_field] = output
                print " ran csv processor and got : " + str(output)
        except Exception:
            pass
        finally:
            self.close_file()

        return result_collector

    def get_file(self):
        pass

    def close_file(self):
        pass
