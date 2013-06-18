from ckan import model
from ckan.lib.base import (request,
                           render,
                           model,
                           abort, h, g, c)
import ckanext.datastore.logic.action as datastore
from ckan.model import Session
import pylons
from pylons import config
import ckanext.datastore.db as db

class Datastored(object):
	resource_id = None
	lat_col = None
	lng_col = None
	geo_col = 'geometry'
	connection_url = None

	def __init__(self,resource_id,lat_field,lng_field):
		self.resource_id = resource_id
		self.lat_col = lat_field
		self.lng_col = lng_field
		self.connection_url = pylons.config.get('ckan.datastore.write_url')

		if not self.connection_url:
			raise ValueError("Expected datastore write url to be configured in development.ini")

	def publish(self):
		context = { 'model':model,'session':Session, 'user':c.user }
		datastore_exists= datastore.datastore_search(context,{ 'resource_id':self.resource_id,'limit':1 })>0
		
		if not datastore_exists:
			return False

		conn_params = { 'connection_url':self.connection_url,'resource_id':self.resource_id }
		engine = db._get_engine(None, conn_params)
		context['connection'] = engine.connect()
		fields = db._get_fields(context,conn_params)

		if self.geo_col not in fields:
			fields.append({'id': self.geo_col, 'type': u'geometry' })
			trans = context['connection'].begin()
			new_column_res = context['connection'].execute(
						"SELECT AddGeometryColumn('public', '"+self.resource_id+
						"', '"+ self.geo_col+"', 4326, 'GEOMETRY', 2)")
			trans.commit()
			return True

		return True