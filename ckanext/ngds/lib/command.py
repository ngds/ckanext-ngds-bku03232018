''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

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
        else:
            print "Command %s not recognized" % cmd

