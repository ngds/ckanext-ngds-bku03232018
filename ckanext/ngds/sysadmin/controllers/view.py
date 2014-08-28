from ckanext.ngds.common import plugins as p
from ckanext.ngds.common import helpers as h
from ckanext.ngds.common import base

class ViewController(base.BaseController):

    def homepage_search(self):
        data = base.request.params
        query = ''

        if 'query' in data:
            query = data['query']

        if data['search-type'] == 'catalog_search':
            controller = ''
            return h.url_for(controller)