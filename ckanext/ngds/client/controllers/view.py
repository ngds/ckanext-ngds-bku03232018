import ckan.plugins as p
from ckan import model
from ckan.lib.base import BaseController, abort, response
from pylons.i18n import _

class ViewController(BaseController):
    """
    Controller object for rendering custom NGDS views and templates.
    @param BaseController: Vanillan CKAN object for extending controllers.
    """