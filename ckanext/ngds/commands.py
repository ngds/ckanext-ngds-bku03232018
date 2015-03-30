import collections
import os
import sys
import re
import csv
import datetime
import json
import urllib
import lxml.etree
import ckan
import ckan.model as model
import ckan.logic as logic
import ckan.lib.search as search
import ckan.logic.schema as schema
import ckan.lib.cli as cli
import requests
import ckanext.harvest.model as harvest_model
from ckanext.harvest.model import HarvestSource, HarvestJob
import xml.etree.ElementTree as ET
import ckan.lib.munge as munge
import ckan.plugins as p
from pylons import config
from urllib2 import Request, urlopen, URLError, HTTPError
import time
import math

import logging
log = logging.getLogger()

class NgdsCommand(cli.CkanCommand):
    '''
    Commands:

        paster ngds purge-deleted-harvest-sources -c <config>
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

    def purge_deleted_harvest_sources(self):
        ''' Hard delete or purge harvest sources that have been deactivated'''

        from ckan.lib.cli import DatasetCmd

        print str(datetime.datetime.now()) + ' Starting harvester source  purge'

        sql  = 'SELECT id, state, type FROM package;'
        rows = model.Session.execute(sql)

        for row in rows:
            if row.state == 'deleted' and row.type == 'harvest':
                dataset_cmd = DatasetCmd('ngds_harvester_source_delete')
                dataset_cmd.purge(row.id)

        print str(datetime.datetime.now()) + ' Finished harvester source  purge'
