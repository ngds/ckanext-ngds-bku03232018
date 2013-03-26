from ckan.lib.base import *
from ckan.lib.base import (request,
                           render,
                           BaseController,
                           model,
                           abort, h, g, c)

import json
from pylons.decorators import jsonify
from ckanext.ngds.ngdsui.controllers.ngds import NGDSBaseController
from ckanext.ngds.ngdsui.lib.poly import get_package_ids_in_poly


class MapController(NGDSBaseController):
	@jsonify
	def test(self):
		temp_par = []
		poly_par = []
		poly_template_str = ''
		decoder = json.JSONDecoder()
		encoder = json.JSONEncoder()
		x = decoder.decode(request.params['data'])
		db_srid = int(config.get('ckan.spatial.srid', '4326'))
		ids = get_package_ids_in_poly(x,db_srid)
		# output = dict(count=len(ids),results=ids)
		return { "results":ids }
		