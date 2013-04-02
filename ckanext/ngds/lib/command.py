from ckan.lib.cli import CkanCommand
from ckanext.ngds.lib.importer.importer import BulkUploader

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
            bulkLoader = BulkUploader()
            bulkLoader.importpackagedata(file_path=self.args[1],resource_dir=self.args[2])
        else:
            print "Command %s not recognized" % cmd