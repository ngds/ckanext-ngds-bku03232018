from ckan.lib.base import *
from ckan.lib.base import (request,
                           render,
                           BaseController,
                           model,
                           abort, h, g, c)

class HomeController(BaseController):

	def render_index(self):
		"""	
		Render the home/index page
		"""
		return render('home/index_ngds.html')

	def render_about(self):
		"""	
		Render the about page
		"""
		return render('home/about_ngds.html')


	def render_map(self):
		
		"""
		Renders the given page. This method is a temporary one & needs to be removed once the actual navigations are defined.
		"""
		return render('map/map.html')	

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
		
