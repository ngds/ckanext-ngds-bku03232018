from ckan.lib.base import *
from ckan.lib.navl.dictization_functions import DataError, unflatten, validate
from ckan.lib.base import (request,
                           render,
                           BaseController,
                           model,
                           abort, h, g, c)
from ckan.model.resource import Resource
import ckanext.ngds.geoserver.logic.action as action
from pylons import config
from pylons.decorators import jsonify
from ckan.logic import (tuplize_dict,clean_dict,
                        parse_params,flatten_to_string_key,get_action,check_access,NotAuthorized)
from ckan.controllers.storage import StorageController,StorageAPIController
import ckan.controllers.storage as storage
import json
import ckanext.ngds.contentmodel
import ckanext.ngds.contentmodel.shp2pg as shapefile
import sys

from ckanext.datastore.logic import action as datastoreaction

class OGCController(BaseController):

    @jsonify
    def publish_ogc(self):
        context = {'model': model, 'session': model.Session,'user': c.user or c.author}
        data = clean_dict(unflatten(tuplize_dict(parse_params(request.params))))
        res = Resource().get(data['id'])
        uri = Resource().get(data['id']).extras['content_model_version']
        url = res.url

        print "---------------------------------------------------------------------->"
        print "CONTEXT: "
        print context
        print "DATA: "
        print data
        print "RESOURCE: "
        print res
        print "URI: "
        print uri
        print "URL: "
        print url
        print "---------------------------------------------------------------------->"

        if url[len(url)-3:len(url)] == 'zip':
            action.shapefile_expose_as_layer(context, data)



        if url[len(url)-3:len(url)]=='csv':
            action.datastore_spatialize(context,data)

        return {
            'success':True,
            'url':url
        }
