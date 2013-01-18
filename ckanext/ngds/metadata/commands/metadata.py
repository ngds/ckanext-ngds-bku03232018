from ckan.lib.cli import CkanCommand
import logging
log = logging.getLogger(__name__)

class Metadata(CkanCommand):
    """
    Performs paster commands
    """
    
    summary = "Install databases"
    usage = __doc__
    max_args = 2
    min_args = 0
    
    def command(self):
        self._load_config()
        cmd = self.args[0]
        if cmd == "initdb":
            self.initdb()
        else:
            print "Command %s not recognized" % cmd
            
    def initdb(self):
        """Paster routine to build database tables"""
        from ckanext.ngds.metadata.model.additional_metadata import db_setup
        db_setup()
        