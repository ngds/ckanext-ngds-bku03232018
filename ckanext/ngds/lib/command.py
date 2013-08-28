from ckan.lib.cli import CkanCommand

class APICommand(CkanCommand):
    """
    Handles various processes in the system.

    ngdsapi import           - alias of initiating Bulk Upload process
    ngdsapi doc-index        - Initiating Full-text Indexing process

    """
    summary = "General Command"
    usage = __doc__
    max_args = 4
    min_args = 0
    
    def command(self):
        self._load_config()
        cmd = self.args[0]
        if cmd == "import":
            from ckanext.ngds.lib.importer.importer import BulkUploader
            bulkLoader = BulkUploader()
            bulkLoader.execute_bulk_upload()
        elif cmd == "doc-index":
            from ckanext.ngds.ngdsui.misc.helpers import process_resource_docs_to_index
            process_resource_docs_to_index()
        else:
            print "Command %s not recognized" % cmd

