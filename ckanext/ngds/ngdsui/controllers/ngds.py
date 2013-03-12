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


		g.logo_text = config.get('ngds.logo_text', 'REDUCE RISK, INCREASE CERTAINTY')

		ngds_deployment = config.get('ngds.deployment', 'central')

		g.default_group = config.get('ngds.default_group_name', 'public')

		g.node_in_a_box = False
		g.central = False

		if ngds_deployment == 'node':
			g.node_in_a_box = True
		else:
			g.central = True