from ckanext.ngds.common import plugins as p
from ckanext.ngds.common import base

class ViewController(base.BaseController):
    """
    Controller object for rendering custom NGDS views and templates.
    @param BaseController: Vanillan CKAN object for extending controllers.
    """

    def render_harvest(self):
        pass

    def render_developers(self):
        pass

    def render_help(self):
        pass

    def render_contact(self):
        pass