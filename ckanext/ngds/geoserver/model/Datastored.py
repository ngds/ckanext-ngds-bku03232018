from pylons import config
import ckanext.datastore.db as db
from ckan.plugins import toolkit
from sqlalchemy.exc import ProgrammingError
import logging
log = logging.getLogger(__name__)

class Datastored(object):
    resource_id = None
    lat_col = None
    lng_col = None
    geo_col = 'geometry'
    connection_url = None

    def __init__(self, resource_id, lat_field, lng_field):
        self.resource_id = resource_id
        self.lat_col = lat_field
        self.lng_col = lng_field
        self.connection_url = config.get('ckan.datastore.write_url')

        if not self.connection_url:
            raise ValueError("Expected datastore write url to be configured in development.ini")

    def publish(self):
        # Get the connection parameters for the datastore
        conn_params = {'connection_url': self.connection_url, 'resource_id': self.resource_id}
        engine = db._get_engine(None, conn_params)
        connection = engine.connect()

        try:
            # This will fail with a ProgrammingError if the table does not exist
            fields = db._get_fields({"connection": connection}, conn_params)
        except ProgrammingError as ex:
            raise toolkit.ObjectNotFound("Resource not found in datastore database")

        # If there is not already a geometry column...
        if True not in map(lambda col: col["id"] == self.geo_col, fields):
            # ... append one
            fields.append({'id': self.geo_col, 'type': u'geometry'})

            # SQL to create the geometry column
            sql = "SELECT AddGeometryColumn('public', '%s', '%s', 4326, 'GEOMETRY', 2)" % (self.resource_id, self.geo_col)

            # Create the new column
            trans = connection.begin()
            connection.execute(sql)
            trans.commit()

            log.info("Created column geometry for table %s" % self.resource_id)

            # Update values in the Geometry column
            sql = "UPDATE \"%s\" SET \"%s\" = geometryfromtext('POINT(' || \"%s\" || ' ' || \"%s\" || ')', 4326)"
            sql = sql % (self.resource_id, self.geo_col, self.lng_col, self.lat_col)

            trans = connection.begin()
            connection.execute(sql)
            trans.commit()

            return True

        log.info("Nothing to do. Returning.")
        return False

    def table_name(self):
        return self.resource_id