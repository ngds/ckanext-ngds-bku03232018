import logging
import pylons
import ckan.logic as logic
import ckan.plugins as p
import ckanext.datastore.db as db
# //Q: Import the newly created function to get all fields of a table
#from ckanext.datastore.db import get_fields
import sqlalchemy

log = logging.getLogger(__name__)
_get_or_bust = logic.get_or_bust


def datastore_spatialize(context, data_dict):
    '''Spatializes a table in the datastore

    The datastore_spatialize API action allows a user to add a column of type GeoPoint
    to an existing datastore resource and fill that column with meaningful values. The 
    values are calculated out of other columns that represent geographic positions as
    latitude and longitude.
    
    In order for the *spatialize* methods to work, a unique key has to be defined via
    the datastore_create action. The available methods are:

    *spatialize*
        It first checks if the GeoPoint column already exists. If not it creates it.
        Afterwards it iterates through all rows and updates the value of the GeoPoint 
        column.

    :param resource_id: resource id that the data is going to be stored under.
    :type resource_id: string
    :param col_latitude: the column containing the latitude values.
    :type column_id: string
    :param col_longitude: the column containing the longitude values.
    :type column_id: string
    :param col_geography: the column that shall be filled with the GeoPoint values.
    :type column_id: string
    
    **Results:**

    :returns: The modified data objects.
    :rtype: dictionary

    
    '''
    if 'id' in data_dict:
        data_dict['resource_id'] = data_dict['id']
    res_id = _get_or_bust(data_dict, 'resource_id')
       
    data_dict['connection_url'] = pylons.config['ckan.datastore.write_url']

    # verifies if the provided resource_id exists in teh database
    resources_sql = sqlalchemy.text(u'''SELECT 1 FROM "_table_metadata"
                                        WHERE name = :id AND alias_of IS NULL''')
    results = db._get_engine(None, data_dict).execute(resources_sql, id=res_id)
    res_exists = results.rowcount > 0

    if not res_exists:
        raise p.toolkit.ObjectNotFound(p.toolkit._(
            'Resource "{0}" was not found.'.format(res_id)
        ))

    # verifies if the user calling the method has permission to execute it
    p.toolkit.check_access('datastore_spatialize', context, data_dict)

    # We now verify if the resource has the geography column.
    # if it does not have it, we create taht column.
    engine = db._get_engine(None, data_dict)
    context['connection'] = engine.connect()
    fields = db._get_fields(context, data_dict)
    try:
        already_has_geography = False
        for field in fields:
            #print field['id']
            if field['id'] == data_dict['col_geography']:
                already_has_geography = True
    
        if not already_has_geography:
            # add geography colum to the list of fields
            # the list of fields is part of the returned result
            fields.append({'id': data_dict['col_geography'],'type': u'geometry' })
            data_dict['fields'] = fields
            
            # create the geography colum in the table
            trans = context['connection'].begin()
            new_column_res = context['connection'].execute(
                        "SELECT AddGeometryColumn('public', '"+data_dict['resource_id']+
                        "', '"+ data_dict['col_geography']+"', 4326, 'GEOMETRY', 2)")
            trans.commit()

        # call a stored procedure from postgis to convert the longitude and latitude
        # columns into a geography shape
        trans = context['connection'].begin()
        spatialize_sql = sqlalchemy.text("UPDATE \"" 
                                         + data_dict['resource_id'] 
                                         + "\" SET \"" 
                                         + data_dict['col_geography'] 
                                         + "\" = geometryfromtext('POINT(' || \"" 
                                         + data_dict['col_longitude'] 
                                         + "\" || ' ' || \"" 
                                         + data_dict['col_latitude'] + "\" || ')', 4326)")
        
        # this return is of type engine.ResultProxy
        # rows are accessed by calling row = proxy.fetchone()
        # col = row[0] or by row['row_name']
        # optionally one can call the command fetchall() with returns a list of rows
        spatialize_results = db._get_engine(None, data_dict).execute(spatialize_sql) 
        trans.commit()

        trans = context['connection'].begin()    
        newtable = context['connection'].execute(
                   u'SELECT * FROM pg_tables WHERE tablename = %s',data_dict['resource_id'])
        
        # add the content of the modified table to the data dictionary, and return it.
        # utilize the standard json format
        formatted_results = db.format_results(context, newtable, data_dict)
        trans.commit()
    
        formatted_results.pop('id', None)
        formatted_results.pop('connection_url')
        return formatted_results
        
        
    except Exception, e:
        trans.rollback()
        if 'due to statement timeout' in str(e):
            raise ValidationError({
                'query': ['Query took too long']
            })
        raise
    finally:
        context['connection'].close()
    
