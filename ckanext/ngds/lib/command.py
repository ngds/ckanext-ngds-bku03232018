from ckan.lib.cli import CkanCommand
import ckanext.ngds.lib.importer.importer as spreadsheet_importer

class APICommand(CkanCommand):
    """
    Performs paster commands
    """
    summary = "General Command"
    usage = __doc__
    max_args = 3
    min_args = 0
    
    def command(self):
        self._load_config()
        cmd = self.args[0]
        if cmd == "import":
            print "File Path: ",self.args[1]
            spreadsheet_importer.importrecordclient(self.args[1])
        else:
            print "Command %s not recognized" % cmd