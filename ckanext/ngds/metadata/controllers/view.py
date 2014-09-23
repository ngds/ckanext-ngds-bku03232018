from ckanext.ngds.common import plugins as p
from ckanext.ngds.common import model
from ckanext.ngds.common import base
from ckanext.ngds.common import pylons_i18n

class ViewController(base.BaseController):
    """
    Controller object for rendering an ISO 19139 XML representation of a CKAN
    package.
    @param BaseController: Vanilla CKAN object for extending controllers
    """
    def show_iso_19139(self, id):
        """
        Given a CKAN package ID: scrape the package data, parse data in the
        'iso_metadata' function, set response parameters and return an ISO
        19139 XML representation of the CKAN package.  On error, return an
        appropriate HTTP error status code.

        @param id: The ID of a CKAN package
        @return: ISO 19139 XML representation of CKAN package
        """
        try:
            context = {'model': model, 'user': base.c.user}
            obj = p.toolkit.get_action('iso_19139')(context, {'id': id})
            base.response.content_type = 'application/xml; charset=utf-8'
            base.response.headers['Content-Length'] = len(obj)
            return obj.encode('utf-8')

        except p.toolkit.ObjectNotFound, e:
            base.abort(404, pylons_i18n._(str(e)))
        except p.toolkit.NotAuthorized:
            base.abort(401, self.not_auth_message)
        except Exception, e:
            msg = 'An error ocurred: [%s]' % str(e)
            base.abort(500, msg)