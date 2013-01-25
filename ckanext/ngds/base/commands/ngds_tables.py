from ckan.lib.cli import CkanCommand
from ckan import model

class NgdsTables(CkanCommand):
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
        
        # Setup additional metadata tables
        from ckanext.ngds.metadata.model.additional_metadata import db_setup as setup_metadata_tables
        setup_metadata_tables()
        
def create_tables(tables, log):
    """Given a list of table definition objects, create those tables in the database"""
    def create_table(table):
        """Creates a single table in the database"""
        if not table.exists():
            try:
                table.create()
            except Exception, e:
                raise e
            log.debug('Created %s table' % table.name)
        else:
            log.debug('%s table already exists' % table.name)
            pass
        
    if model.package_table.exists(): # check that the Package table exists
        for table in tables:
            create_table(table) # Create each of the tables
    else:
        log.debug('Additional table creation deferred - install the base CKAN tables first.')
        pass
        