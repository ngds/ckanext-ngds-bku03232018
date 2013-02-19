from ckan.plugins import implements, SingletonPlugin, IRoutes, IConfigurer, toolkit

class NgdsuiPlugin(SingletonPlugin):
	implements(IRoutes,inherit=True)
	implements(IConfigurer,inherit=True)

	def before_map(self,map):
		"""
		For the moment, set up routes under the sub-root /ngds to render the UI.
		"""
		home_controller = "ckanext.ngds.ngdsui.controllers.home:HomeController"
		map.connect("home","/ngds",controller=home_controller,action="render_index",conditions={"method":["GET"]})
		map.connect("about","/ngds/about",controller=home_controller,action="render_about",conditions={"method":["GET"]})


		contribute_controller = "ckanext.ngds.ngdsui.controllers.contribute:ContributeController"
		map.connect("contribute","/ngds/contribute",controller=contribute_controller,action="index")
		map.connect("harvest","/ngds/harvest",controller=contribute_controller,action="harvest")
		map.connect("harvest_new","/ngds/harvest/{action}",controller=contribute_controller)
		# map.connect("upload","/ngds/contribute/upload",controller=contribute_controller,action="upload")
		map.redirect('/ngds/contribute/dataset/{action}', '/dataset/{action}')
		#map.connect("harvest_new","/ngds/harvest/edit",controller="ckanext.ngds.ngdsui.controllers.contribute:ContributeController",action="edit")

		map.connect("harvest","/ngds/harvest/{id}/{action}",controller=contribute_controller)

		#Map related paths
		map.connect("map","/ngds/map",controller=home_controller,action="render_map",conditions={"method":["GET"]})
		map.connect("library","/ngds/library",controller=home_controller,action="render_library",conditions={"method":["GET"]})
		map.connect("resources","/ngds/resources",controller=home_controller,action="render_resources",conditions={"method":["GET"]})
		map.connect("search","/ngds/library/search",controller='package',action="search")

		return map

	def update_config(self,config):
		"""
		Register the templates directory with ckan so that Jinja can find them.
		"""
		toolkit.add_template_directory(config,'templates')
		#Static files are to be served up from here. Otherwise, pylons will try and decode content in here and will fail.
		toolkit.add_public_directory(config,'public')