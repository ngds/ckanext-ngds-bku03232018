''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

"""
This is the base controller object which other controllers extend.
"""
from ckan.lib.base import *
from ckan.lib.base import (request,
                           render,
                           BaseController,
                           model,
                           abort, h, g, c)
import sqlalchemy.exc
from pylons import config


class NGDSBaseController(BaseController):
    def __before__(self, action, **env):
        try:
            BaseController.__before__(self, action, **env)

            self._ngds_deployment()
        except (sqlalchemy.exc.ProgrammingError,
                sqlalchemy.exc.OperationalError), e:
            # postgres and sqlite errors for missing tables
            msg = str(e)
            if ('relation' in msg and 'does not exist' in msg) or \
                    ('no such table' in msg):
                # table missing, major database problem
                abort(503, _('This site is currently off-line. Database is not initialised.'))
            else:
                raise


    def _ngds_deployment(self):
        """
        Retreive configuration items that will be essential to the application while it is running. These are :
        1) Logo text to display below the site-logo.
        2) The deployment configuration of this node to determine if this is a node-in-a-box deployment or a central node deployment,
            what functionality must be exposed and what pages to render.
        3) The default group name under which all datasets will be stored. This information is purely internal and not exposed to the user.
        """
        g.logo_text = config.get('ngds.logo_text', 'REDUCE RISK, INCREASE CERTAINTY')

        ngds_deployment = config.get('ngds.deployment', 'central')

        g.default_group = config.get('ngds.default_group_name', 'public')

        g.node_in_a_box = False
        g.central = False

        if ngds_deployment == 'node':
            g.node_in_a_box = True
        else:
            g.central = True
