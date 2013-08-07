from ckan.lib.cli import CkanCommand

class APICommand(CkanCommand):
    """
    Performs paster commands
    """
    summary = "General Command"
    usage = __doc__
    max_args = 4
    min_args = 0
    
    def command(self):
        self._load_config()
        cmd = self.args[0]
        #print "Arguments: ",self.args
        if cmd == "import":
            #print "File Path: ",self.args[1]
            from ckanext.ngds.lib.importer.importer import BulkUploader
            bulkLoader = BulkUploader()
            #bulkLoader.importpackagedata(file_path=self.args[1],resource_dir=self.args[2])
            bulkLoader.execute_bulk_upload()
        elif cmd == "doc-index":
            from ckanext.ngds.ngdsui.misc.helpers import process_resource_docs_to_index
            process_resource_docs_to_index()

        else:
            print "Command %s not recognized" % cmd

