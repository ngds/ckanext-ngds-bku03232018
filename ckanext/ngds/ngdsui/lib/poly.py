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