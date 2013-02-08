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
			self._isUser_isAdmin()
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

		ngds_deployment = config['ngds_deployment'] or 'central'

		print "Deployment : "+ngds_deployment
		
		if ngds_deployment == 'node':
			c.node_in_a_box = True
		else:
			c.central = True

		
 	def _isUser_isAdmin(self):
 		"""
 		This method checks whether user logged in and his access details.
 		If the user is logged in then sets c.user_logged_in as 'True'.
 		If the user is admin then sets c.admin as 'True'
 		"""
 		user_access = config['user_access'] or 'admin'

 		if user_access == 'admin':
 			c.admin = True
 		else:
 			c.admin = False
 			
 		c.user_logged_in = True