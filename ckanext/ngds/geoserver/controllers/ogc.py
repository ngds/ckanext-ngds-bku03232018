from ckan.lib.navl.dictization_functions import unflatten
from ckan.lib.base import (request, BaseController, model, c)
from ckan.model.resource import Resource
import ckanext.ngds.geoserver.logic.action as action

from pylons.decorators import jsonify
from ckan.logic import (tuplize_dict, clean_dict, parse_params)

class OGCController(BaseController):

    @jsonify
    def publish_ogc(self):
        """
        Publishes the resource content into Geoserver. Shape file and csv files are handled differently.
        """
        context = {'model': model, 'session': model.Session, 'user': c.user or c.author}
        data = clean_dict(unflatten(tuplize_dict(parse_params(request.params))))
        res = Resource().get(data['id'])
        uri = Resource().get(data['id']).extras['content_model_version']
        url = res.url

        if url[len(url)-3:len(url)] == 'zip':
            action.shapefile_expose_as_layer(context, data)

        if url[len(url)-3:len(url)]=='csv':
            action.datastore_spatialize(context,data)

        return {
            'success':True,
            'url':url
        }
