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

    This is what this function does:
    1. Check if the resource exists and if we have access rights (copy from other actions)
    2. call db.py:create to add the additional column to the table
    3. call db.py:??? to update the newly created column

    '''
    if 'id' in data_dict:
        data_dict['resource_id'] = data_dict['id']
    res_id = _get_or_bust(data_dict, 'resource_id')
    
    print ">>>>>>>>>>>>>>>>>>>>>>>> spatialize >>>>>>>>>>>>>>>>>>>>>>>"
    
    data_dict['connection_url'] = pylons.config['ckan.datastore.write_url']

    resources_sql = sqlalchemy.text(u'''SELECT 1 FROM "_table_metadata"
                                        WHERE name = :id AND alias_of IS NULL''')
    results = db._get_engine(None, data_dict).execute(resources_sql, id=res_id)
    res_exists = results.rowcount > 0

    print ">>>>>>>>>>>>>>>>>>>>>>>> before object not found >>>>>>>>>>>>>>>>>>>>>>>"
    
    if not res_exists:
        raise p.toolkit.ObjectNotFound(p.toolkit._(
            'Resource "{0}" was not found.'.format(res_id)
        ))

    print ">>>>>>>>>>>>>>>>>>>>>>>> before check access >>>>>>>>>>>>>>>>>>>>>>>"
    
    # one needs the same authorization as for the create method
    p.toolkit.check_access('datastore_spatialize', context, data_dict)

    print ">>>>>>>>>>>>>>>>>>>>>>>> after check_access >>>>>>>>>>>>>>>>>>>>>>>"

    #geography_col = data_dict['col_geography']
    #latitude_col = data_dict['col_latitude']
    #longitude_col = data_dict['col_longitude']

    print ">>>>>>>>>>>>>>>>>> calling get_fields >>>>>>>>>>>>>>>>>>>>>>>>>"
    # We have to include a 'connection' attribute in the context
    engine = db._get_engine(None, data_dict)
    context['connection'] = engine.connect()
    fields = db._get_fields(context, data_dict)
    
    print ">>>>>>>>>>>>>>>>>> fields begin >>>>>>>>>>>>>>>>>>>>>>>>>"
    already_has_geography = False
    for field in fields:
        print field['id']
        if field['id'] == data_dict['col_geography']:
            already_has_geography = True
    print ">>>>>>>>>>>>>>>>>> fields end >>>>>>>>>>>>>>>>>>>>>>>>>"

    if not already_has_geography:
        print ">>>>>>>>>>>>>>>>>> adding geography field >>>>>>>>>>>>>>>>>>>>>>>>>" 
        #fields.append({'id': data_dict['col_geography'],'type': u'numeric' })
        fields.append({'id': data_dict['col_geography'],'type': u'GEOGRAPHY(Point)' })
        data_dict['fields'] = fields
        result = db.create(context, data_dict)
    else:
        print ">>>>>>>>>>>>>>>>>> skip adding geography field >>>>>>>>>>>>>>>>>>>>>>>>>"
        
    
    print ">>>>>>>>>>>>>>>>>>>>>>>> convert long/lat into point >>>>>>>>>>>>>>>>>>>>>>>"
    # spatialize_sql = sqlalchemy.text("UPDATE \":t\" SET :geo = ST_GeogFromText('POINT(' || :long || ' ' || :lat || ')')")       
    # spatialize_sql = sqlalchemy.text("UPDATE :t SET :geo = ST_GeogFromText('SRID=4326;POINT(' || :long || ' ' || :lat || ')')")
    spatialize_sql = sqlalchemy.text("UPDATE \"" + data_dict['resource_id'] + "\" SET \"" + data_dict['col_geography'] + "\" = ST_GeogFromText('SRID=4326;POINT(' || \"" + data_dict['col_longitude'] + "\" || ' ' || \"" + data_dict['col_latitude'] + "\" || ')')")
    print spatialize_sql        
    print data_dict['resource_id']               
    
    result = db._get_engine(None, data_dict).execute(spatialize_sql)
#    result = db._get_engine(None, data_dict).execute(spatialize_sql,
#                                                      t=data_dict['resource_id'],
#                                                      geo=data_dict['col_geography'],
#                                                      long=data_dict['col_longitude'],
#                                                      lat=data_dict['col_latitude'])

    print ">>>>>>>>>>>>>>>>>>>>>>> check >>>>>>>>>>>>>>>>>>>>>>>>>>"
    
    #result.pop('id', None)
    #result.pop('connection_url')
    return result
