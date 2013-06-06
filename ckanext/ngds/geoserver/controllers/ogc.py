from ckan.lib.base import *
from ckan.lib.navl.dictization_functions import DataError, unflatten, validate
from ckan.lib.base import (request,
                           render,
                           BaseController,
                           model,
                           abort, h, g, c)
from ckan.model.resource import Resource
from pylons import config
from pylons.decorators import jsonify
from ckan.logic import (tuplize_dict,clean_dict,
                        parse_params,flatten_to_string_key,get_action,check_access,NotAuthorized)
from ckan.controllers.storage import StorageController,StorageAPIController
import json

class OGCController(BaseController):

	@jsonify
	def publish_ogc(self):
		data = clean_dict(unflatten(tuplize_dict(parse_params(
            request.params))))	
		res = Resource().get(data['id'])
		url = res.url
		print url
		if url[len(url)-3:len(url)]=='zip':
			print "ZIp"
		return {
			'success':True,
			'url':url
		}