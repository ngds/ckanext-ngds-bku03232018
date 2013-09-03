from pylons import config
import ckanext.datastore.db as db
from ckan.plugins import toolkit
from sqlalchemy.exc import ProgrammingError
import logging
log = logging.getLogger(__name__)

class Datastored(object):
    """
    Handles the resources which are loaded by Datastore extension. Makes the details available for Geoserver to access.
    """

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
            raise ValueError(toolkit._("Expected datastore write url to be configured in development.ini"))

    def publish(self):
        """
        Checks and generates the 'Geometry' column in the table for Geoserver to work on.
        Resource in datastore database is checked for Geometry field. If the field doesn't exists then calculates the
        geometry field value and creates it in the table.
        """

        # Get the connection parameters for the datastore
        conn_params = {'connection_url': self.connection_url, 'resource_id': self.resource_id}
        engine = db._get_engine(None, conn_params)
        connection = engine.connect()

        try:
            # This will fail with a ProgrammingError if the table does not exist
            fields = db._get_fields({"connection": connection}, conn_params)
        except ProgrammingError as ex:
            raise toolkit.ObjectNotFound(toolkit._("Resource not found in datastore database"))

        # If there is not already a geometry column...
        if not True in { col['id'] == self.geo_col for col in fields }:
            # ... append one
            fields.append({'id': self.geo_col, 'type': u'geometry'})

            # SQL to create the geometry column
            sql = "SELECT AddGeometryColumn('public', '%s', '%s', 4326, 'GEOMETRY', 2)" % (self.resource_id, self.geo_col)

            # Create the new column
            trans = connection.begin()
            connection.execute(sql)
            trans.commit()

            # Update values in the Geometry column
            sql = "UPDATE \"%s\" SET \"%s\" = geometryfromtext('POINT(' || \"%s\" || ' ' || \"%s\" || ')', 4326)"
            sql = sql % (self.resource_id, self.geo_col, self.lng_col, self.lat_col)

            trans = connection.begin()
            connection.execute(sql)
            trans.commit()

            return True

        return True

    def table_name(self):
        return self.resource_id