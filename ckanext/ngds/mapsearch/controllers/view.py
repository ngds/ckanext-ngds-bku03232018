from ckanext.ngds.common import base
from ckanext.ngds.common import plugins as p

class ViewController(base.BaseController):
    """
    Controller object for rendering custom NGDS views and templates.
    @param BaseController: Vanillan CKAN object for extending controllers.
    """
    def render_map_search(self):
        return p.toolkit.render('mapsearch/map_search.html')

    def render_library_search(self):
        pass

    def render_contribute(self):
        pass

    def render_help(self):
        pass
