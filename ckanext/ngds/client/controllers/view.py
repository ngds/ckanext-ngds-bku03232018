from ckanext.ngds.common import plugins as p
from ckanext.ngds.common import base

class ViewController(base.BaseController):
    """
    Controller object for rendering custom NGDS views and templates.
    @param BaseController: Vanillan CKAN object for extending controllers.
    """

    def render_developers(self):
        return p.toolkit.render('ngds/developers.html')

    def render_help(self):
        return p.toolkit.render('ngds/help.html')

    def render_contact(self):
        return p.toolkit.render('ngds/contact.html')