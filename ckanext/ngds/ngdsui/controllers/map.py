from ckan.lib.base import *
from ckan.lib.base import (request,
                           render,
                           BaseController,
                           model,
                           abort, h, g, c)
from ckanext.spatial.model import PackageExtent
from shapely.geometry import asShape
from ckan.model import Session, Package
import json
from pylons.decorators import jsonify
from ckanext.ngds.ngdsui.controllers.ngds import NGDSBaseController

from geoalchemy import WKTSpatialElement

class MapController(NGDSBaseController):
	@jsonify
	def test(self):
		temp_par = []
		poly_par = []
		i=0
		poly_template_str = ''
		decoder = json.JSONDecoder()
		encoder = json.JSONEncoder()
		x = decoder.decode(request.params['data'])
		for item in x['poly']:
			print item
			if i==0:
				poly_template_str = poly_template_str + ''+str(item[1]) +' '+ str(item[0])+', '
			elif i==len(x['poly'])-1:
				poly_template_str = poly_template_str +''+str(item[1]) +' '+ str(item[0])
			else:
				poly_template_str = poly_template_str +''+str(item[1]) +' '+ str(item[0])+', '
			i=i+1

		poly_template_str = 'POLYGON (('+poly_template_str + ', '+str(x['poly'][0][1]) +' '+ str(x['poly'][0][0])+'))'
		db_srid = int(config.get('ckan.spatial.srid', '4326'))

	    # bbox_template = Template('POLYGON (($minx $miny, $minx $maxy, $maxx $maxy, $maxx $miny, $minx $miny))')

		wkt = poly_template_str

		input_geometry = WKTSpatialElement(wkt,db_srid)

		extents = Session.query(PackageExtent).filter(PackageExtent.package_id==Package.id).filter(PackageExtent.the_geom.intersects(input_geometry)).filter(Package.state==u'active').all()
		
		ids = [extent.package_id for extent in extents]

		output = dict(count=len(ids),results=ids)
		ids = []
		for extent in extents:
			ids.append(extent.package_id)
		return { "results":ids }
		