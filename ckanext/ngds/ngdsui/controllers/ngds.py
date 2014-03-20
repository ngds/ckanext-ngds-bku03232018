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
