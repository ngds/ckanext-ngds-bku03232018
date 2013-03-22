import logging
import pylons
import ckan.logic as logic
import ckan.plugins as p
import ckanext.datastore.db as db
# //Q: Import the newly created function to get all fields of a table
from ckanext.datastore.db import get_fields
import sqlalchemy

log = logging.getLogger(__name__)
_get_or_bust = logic.get_or_bust


# //Q: This function is introduced to spatialize the database
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

    # We add a new dictionary entry to prepare for the db.create function
    data_dict['fields']= [{'type': u'text', 'id': u'LABEL'}, 
                          {'type': u'numeric', 'id': u'LATITUDE'}, 
                          {'type': u'numeric', 'id': u'LONGITUDE'}, 
                          {'type': u'text', 'id': u'SRS'}, 
                          {'type': u'text', 'id': u'BHT'}, 
                          {'type': u'numeric', 'id': u'DEPTH'}, 
                          {'type': u'text', 'id': u'COUNTY'}, 
                          {'type': u'text', 'id': u'STATE'}, 
                          {'type': u'numeric', 'id': u'ELEVATION'}, 
                          {'type': u'text', 'id': u'COMPANY'}, 
                          {'type': u'numeric', 'id': u'DRILL DEPTH'}, 
                          {'type': u'timestamp', 'id': u'LOG DATE'},
                          {'type': u'numeric', 'id': data_dict['col_geography']}]

    # We are done just copy the results to the dictionary.
    print ">>>>>>>>>>>>>>>>>>>>>>>> before db.create >>>>>>>>>>>>>>>>>>>>>>>"
    fields= get_fields(context, data_dict)
    
    result = db.create(context, data_dict)
    result.pop('id', None)
    result.pop('connection_url')
    return result
