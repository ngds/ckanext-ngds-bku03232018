from ckan.lib.base import *

class HomeController(BaseController):

	def render_index(self):
		"""	
		Render the home/index page
		"""
		return render('home/index_ngds.html',{'active_tab':'home'})

	def render_about(self):
		"""	
		Render the about page
		"""
		return render('home/about_ngds.html')


	def render_map(self):
		
		"""
		Renders the given page. This method is a temporary one & needs to be removed once the actual navigations are defined.
		"""
		return render('map/map.html',{'active_tab':'map'})	

	def render_library(self):
		
		"""
		Renders the given page. This method is a temporary one & needs to be removed once the actual navigations are defined.
		"""
		return render('library/library.html',{'active_tab':'library'})	

	def render_contribute(self):
		
		"""
		Renders the given page. This method is a temporary one & needs to be removed once the actual navigations are defined.
		"""
		return render('contribute/contribute.html',{'active_tab':'contribute'})	

	def render_resources(self):
		
		"""
		Renders the given page. This method is a temporary one & needs to be removed once the actual navigations are defined.
		"""
		return render('resources/resources.html',{'active_tab':'resources'})			 				 				 		
		
