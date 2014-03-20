""" NGDS_HEADER_BEGIN

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey

Please refer the the README.txt file in the base directory of the NGDS project:
https://github.com/ngds/ckanext-ngds/blob/master/README.txt

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero
General Public License as published by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.  https://github.com/ngds/ckanext-ngds
ngds/blob/master/LICENSE.md or
http://www.gnu.org/licenses/agpl.html

NGDS_HEADER_END """

from ckanext.spatial.model import PackageExtent
from shapely.geometry import asShape
from ckan.model import Session, Package
from geoalchemy import WKTSpatialElement

def get_package_ids_in_poly(coords,db_srid):
	"""
	TODO: This needs to be removed as spatial backend is changed to Solr.
	"""
	poly_template_str = ''
	x = coords
	i=0
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

    # bbox_template = Template('POLYGON (($minx $miny, $minx $maxy, $maxx $maxy, $maxx $miny, $minx $miny))')

	wkt = poly_template_str

	input_geometry = WKTSpatialElement(wkt,db_srid)

	extents = Session.query(PackageExtent).filter(PackageExtent.package_id==Package.id).filter(PackageExtent.the_geom.intersects(input_geometry)).filter(Package.state==u'active').all()
	
	ids = [extent.package_id for extent in extents]
	return ids
