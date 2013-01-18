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
        
        from ckan import model
        from ckanext.ngds.metadata.model.additional_metadata import define_tables
        
        party, package_meta, resource_meta = define_tables() # Define the tables
        log.debug('Additional Metadata table defined in memory')
        
        def create_table(table):
            if not table.exists():
                try:
                    table.create()
                except Exception, e:
                    raise e
                
        if model.package_table.exists(): # check that the Package table exists
            for table in [party, package_meta, resource_meta]:
                create_table(table) # Create each of the tables
        else:
            log.debug('Additional table creation deferred - install the base CKAN tables first.')
    
        