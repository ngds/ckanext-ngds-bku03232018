from ckan.lib.base import *
from ckan.lib.navl.dictization_functions import DataError, unflatten, validate
from ckan.lib.base import (request,
                           render,
                           model,
                           abort, h, g, c)
from ckan.logic import get_action,check_access
from ckan.logic import (tuplize_dict,
                        clean_dict,
                        parse_params,
                        flatten_to_string_key)
from pylons import config
from ckanext.ngds.ngdsui.controllers.ngds import NGDSBaseController
from ckan.logic import NotFound, NotAuthorized, ValidationError
from ckanext.ngds.ngdsui.misc import helpers

class UserController(NGDSBaseController):


 	def manage_users(self,group_name='public',data_dict=None):

		"""
		Returns the list of users in the system.
		"""
		context = {'model': model, 'session': model.Session,'user': c.user or c.author}

		try:
			check_access('manage_users',context,data_dict)
		except NotAuthorized, error:
			#abort(401, _('Not authorized to see this page'))
			abort(401,error.__str__())
 
 		group_name = helpers.get_default_group()
		group_members = self.member_list(group_name)

		q = model.Session.query(model.User).\
				filter( ~ model.User.name.in_((model.PSEUDO_USER__LOGGED_IN, model.PSEUDO_USER__VISITOR)))

		def role_lookup(userid,group_members):

			for user_id, role in group_members:
				if user_id == userid :
						return role
			return ""     

		roles = get_action('member_roles_list')(context, {})

		# TODO: Not sure whether this is better way to do .... 
		c.roles = [{'text': u'', 'value': 'default'}]
		c.roles.extend(roles)
		#print "c.roles: ",c.roles
		g.group_name = group_name
		#print "List c.group_id: ",c.group_id
		
		c.members = [(m.id,m.name,m.email,role_lookup(m.id,group_members),)for m in q.all()]   

		return render('user/manage_users.html')


	def logged_out_page(self):
		url = h.url_for(controller='ckanext.ngds.ngdsui.controllers.home:HomeController', action='render_index')
		h.flash_notice(_('You are now Logged out'), allow_html=True)
		redirect(url)
        #return render('user/logout.html')


	def member_new(self,data_dict=None):
		print "Entered update member"		
		context = {'model': model, 'session': model.Session,'user': c.user}
		data_dict = clean_dict(unflatten(tuplize_dict(parse_params(request.params))))

		try:
			check_access('manage_users',context,data_dict)
		except NotAuthorized, error:
			#abort(401, _('Not authorized to see this page'))
			abort(401,error.__str__())

		group = model.Group.get(helpers.get_default_group())

		data_dict['id'] = group.id
		print "data_dict: ",data_dict

		role = data_dict['role']

		if role == 'default':
			get_action('group_member_delete')(context, data_dict)
			h.flash_notice(_('User rights are removed.'), allow_html=True)
		else:
			get_action('group_member_create')(context, data_dict)
			h.flash_success(_('User Role is Updated Successfully.'), allow_html=True)

		url = h.url_for(controller='ckanext.ngds.ngdsui.controllers.user:UserController', action='manage_users')
		redirect(url)


	def member_list(self, group_name):

		#model = context['model']
		#print data_dict
		group = model.Group.get(group_name)
		# g.group_id=group.id

		q = model.Session.query(model.Member).\
				filter(model.Member.group_id == group.id).\
				filter(model.Member.state    == "active").\
				filter(model.Member.table_name == "user")

		return [(m.table_id,m.capacity,)for m in q.all()]