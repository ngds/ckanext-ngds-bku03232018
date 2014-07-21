import ckan.plugins as p
from ckan import model
from ckan.lib.base import BaseController, abort, response, render
from pylons.i18n import _

class ViewController(BaseController):
    """
    Controller object for rendering custom NGDS views and templates.
    @param BaseController: Vanillan CKAN object for extending controllers.
    """
    def render_map_search(self):
        render('mapsearch/map_search.html')

    def render_library_search(self):
        pass

    def render_resources(self):
        pass

    def render_contribute(self):
        pass