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

from ckan.lib.cli import CkanCommand
import os


class APICommand(CkanCommand):
    """
    Handles various processes in the system.

    ngdsapi import           - alias of initiating Bulk Upload process
    ngdsapi doc-index        - Initiating Full-text Indexing process
    ngdsapi compile_client_scripts  -   Minifies javascript resources and compiles project less files to css files

    """
    summary = "General Command"
    usage = __doc__
    max_args = 4
    min_args = 0

    def command(self):
        self._load_config()
        cmd = self.args[0]
        if cmd == "import":
            from ckanext.ngds.importer.importer import BulkUploader

            bulkLoader = BulkUploader()
            bulkLoader.execute_bulk_upload()
        elif cmd == "doc-index":
            from ckanext.ngds.ngdsui.misc.helpers import process_resource_docs_to_index

            process_resource_docs_to_index()
        elif cmd == "compile_client_scripts":
            from ckanext.ngds.lib.compile_client_scripts.script_compiler import ScriptCompiler
            import ckanext.ngds.ngdsui as uimodule

            print ScriptCompiler
            uipath = os.path.dirname(os.path.abspath(uimodule.__file__))
            sc = ScriptCompiler(uipath)
            sc.compile_less()
            sc.minify_js()

        elif cmd == "create_ngds_org":
            from ckanext.ngds.lib.customize.customize import Customize
            cust = Customize()
            cust.customize()
        else:
            print "Command %s not recognized" % cmd

