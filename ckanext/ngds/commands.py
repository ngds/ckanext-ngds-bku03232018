import datetime
import time
import ckan.lib.cli as cli
import ckan.plugins as p
import ckan.logic as logic
import ckan.model as model
from pylons import config
from ckan.lib.cli import DatasetCmd

class NgdsCommand(cli.CkanCommand):
    '''
    Commands:

        paster ngds purge-deleted-harvest-sources -c <config>
        paster ngds purge-deleted-datasets -c <config>
        paster ngds deleted-all-datasets -c <config>
    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__

    def command(self):
        '''
        Parse command line arguments and call appropriate method.
        '''
        if not self.args or self.args[0] in ['--help', '-h', 'help']:
            print NgdsCommand.__doc__
            return

        cmd = self.args[0]
        self._load_config()

        user = logic.get_action('get_site_user')(
            {'model': model, 'ignore_auth': True}, {}
        )
        self.user_name = user['name']

        if cmd == 'purge-deleted-harvest-sources':
            self.purge_deleted_harvest_sources()
        elif cmd == 'purge-deleted-datasets':
            self.purge_deleted_datasets()
        elif cmd == 'dataset-delete-all':
            self.dataset_delete_all()

    def purge_deleted_harvest_sources(self):
        ''' Hard delete or purge harvest sources that have been deactivated'''

        print str(datetime.datetime.now()) + ' Starting harvester source  purge'

        sql  = 'SELECT id, state, type FROM package WHERE state=\'deleted\' AND type=\'harvest\';'
        rows = model.Session.execute(sql)

        for row in rows:
            dataset_cmd = DatasetCmd('ngds_harvester_source_delete')
            dataset_cmd.purge(row.id)

        print str(datetime.datetime.now()) + ' Finished harvester source  purge'

    def purge_deleted_datasets(self):
        ''' Hard delete or purge datasets that have been soft deleted'''

        print str(datetime.datetime.now()) + ' Starting dataset purge'

        sql  = 'SELECT id, state, type FROM package WHERE state=\'deleted\' AND type=\'dataset\' ORDER BY RANDOM();'
        rows = model.Session.execute(sql)

        for row in rows:
            dataset_cmd = DatasetCmd('ngds_dataset_purge')
            dataset_cmd.purge(row.id)

        print str(datetime.datetime.now()) + ' Finished dataset purge'

    def dataset_delete_all(self):
        ''' Soft delete all datasets'''
        
        print str(datetime.datetime.now()) + ' Starting dataset soft delete'

        sql  = 'SELECT id, state, type FROM package WHERE state=\'active\' AND type=\'dataset\';'
        rows = model.Session.execute(sql)

        for row in rows:
            dataset_cmd = DatasetCmd('ngds_dataset_delete')
            dataset_cmd.delete(row.id)

        print str(datetime.datetime.now()) + ' Finished dataset soft delete'
