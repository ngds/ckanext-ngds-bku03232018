import pylons
from pylons import config
import ckanext.datastore.db as db
from ckan.logic import get_action
import sqlalchemy
import logging
log = logging.getLogger(__name__)

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
        if (get_action('datastore_search')(None,{ 'resource_id':self.resource_id,'limit':1 })>0) == False:
            log.debug("Expected datastore connection url to be configured in development.ini")
            return False

        conn_params = { 'connection_url':self.connection_url,'resource_id':self.resource_id }

        engine = db._get_engine(None, conn_params)
        context = { 'connection':engine.connect() }
        fields = db._get_fields(context,conn_params)

        if not True in { col['id'] == self.geo_col for col in fields }:
            fields.append({'id': self.geo_col, 'type': u'geometry' })
            trans = context['connection'].begin()
            new_column_res = context['connection'].execute(
                            "SELECT AddGeometryColumn('public', '"+self.resource_id+
                            "', '"+ self.geo_col+"', 4326, 'GEOMETRY', 2)")
            trans.commit()
            log.info("Created column geometry for table "+self.resource_id)

            trans = context['connection'].begin()
            context['connection'].execute(sqlalchemy.text("UPDATE \""
                                             + self.resource_id
                                             + "\" SET \""
                                             + self.geo_col
                                             + "\" = geometryfromtext('POINT(' || \""
                                             + self.lng_col
                                             + "\" || ' ' || \""
                                             + self.lat_col + "\" || ')', 4326)"))

            # this return is of type engine.ResultProxy
            # rows are accessed by calling row = proxy.fetchone()
            # col = row[0] or by row['row_name']
            # optionally one can call the command fetchall() with returns a list of rows
            trans.commit()
            return True
        log.info("Nothing to do. Returning.")
        return False