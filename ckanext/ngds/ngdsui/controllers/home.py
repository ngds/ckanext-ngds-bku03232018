from ckan.lib.base import *
from ckan.lib.base import (request,
                           render,
                           BaseController,
                           model,
                           abort, h, g, c)

from ckanext.ngds.ngdsui.controllers.ngds import NGDSBaseController
from sqlalchemy import orm, types, Column, Table, ForeignKey, desc, and_
from ckan.controllers.organization import OrganizationController
from ckan.lib.navl.dictization_functions import DataError, unflatten, validate
from ckan.logic import (tuplize_dict,clean_dict,
                        parse_params,flatten_to_string_key,get_action,check_access,NotAuthorized)
from ckan.model import Session, Package
import ckan.logic as logic
import ckan.lib.dictization.model_dictize as model_dictize
from ckan.lib.base import config



class HomeController(NGDSBaseController):

	def render_index(self):
		"""	
		Render the home/index page
		"""

		if g.node_in_a_box:
			return self.render_map()
		
		context = {'model': model, 'session': model.Session, 'user': c.user}
		
		activity_objects = model.Session.query(model.Activity).join(model.Package, model.Activity.object_id == model.Package.id).\
		filter(model.Activity.activity_type == 'new package').order_by(desc(model.Activity.timestamp)).\
		limit(6).all()
		activity_dicts = model_dictize.activity_list_dictize(activity_objects, context)
		# c.recent_activity = logic.get_action('dashboard_activity_list')(
  #           context, {'id': None, 'offset': 0})[1:7]
		c.recent_activity = activity_dicts
		return render('home/index_ngds.html')

	def render_about(self):
		"""	
		Render the about page
		"""
		return render('home/about_ngds.html')


	def render_map(self,query=''):
		
		"""
		Renders the given page. This method is a temporary one & needs to be removed once the actual navigations are defined.
		"""
		return render('map/map.html',{'query':query})	

	def render_library(self):
		
		"""
		Renders the given page. This method is a temporary one & needs to be removed once the actual navigations are defined.
		"""
		return render('library/library.html')	

	def render_resources(self):
		
		"""
		Renders the given page. This method is a temporary one & needs to be removed once the actual navigations are defined.
		"""
		return render('resources/resources.html')

	def initiate_search(self):
		data = clean_dict(unflatten(tuplize_dict(parse_params(
            request.params))))	
		query =''
		if 'query' in data:
			query=data['query']
		if data['search-type']=='library':
			return redirect('/organization/public?q='+query)
		else:
			return self.render_map(query)
		
