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
        
        # Setup CSW table
        from ckanext.ngds.csw.model.csw_records import db_setup as setup_csw_tables
        setup_csw_tables()

        # Setup transaction tables
        from ckanext.ngds.metadata.model.transaction_tables import db_setup as setup_trans_tables
        setup_trans_tables()

        
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
        
