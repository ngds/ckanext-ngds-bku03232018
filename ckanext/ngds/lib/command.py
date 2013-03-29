from ckan.lib.cli import CkanCommand
import ckanext.ngds.lib.importer.importer as spreadsheet_importer

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
        print "Arguments: ",self.args
        if cmd == "import":
            #print "File Path: ",self.args[1]
            spreadsheet_importer.importrecordclient(file_path=self.args[1],resource_dir=self.args[2])
        else:
            print "Command %s not recognized" % cmd