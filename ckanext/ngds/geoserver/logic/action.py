import logging
import pylons
import ckan.logic as logic
import ckan.plugins as p
import ckanext.datastore.db as db
import sqlalchemy
from geoserver.catalog import Catalog
from featuretype import SqlFeatureTypeDef


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
    
        print ">>>>>>>>>>>>>>>>>>>> list exposed layers >>>>>>>>>>>>>>>>>>>>>"    
        # verify if the layer exists in geoserver, if not, create it.


        cat = Catalog('http://localhost:8080/geoserver/rest')
        if cat.get_layer(res_id) is None:
            print ">>>>>>>>>>>>>>>>>>>> create new layer object >>>>>>>>>>>>>>>>>>>>"
            web_url = datastore_expose_as_layer(context, data_dict)
            formatted_results['layer'] = web_url
        else:
            print ">>>>>>>>>>>>>>>>>>>> layer already exists >>>>>>>>>>>>>>>>>>>>"    
        
        '''
        headers= {"Content-type": "text/xml"}
        headers, response = cat.http.request("http://localhost:8080/geoserver/rest/layers", "GET", "", headers)
        if not res_id in response:
            print ">>>>>>>>>> Layer does not exists >>>>>>>>>>>"
            datastore_expose_as_layer(context, data_dict)
        else:
            print ">>>>>>>>>> Layer exists no need to expose it again >>>>>>>>>>>"
        '''
    
    
    
    
    
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
    
    

def datastore_expose_as_layer(context, data_dict):
    '''Publishes an already 'spatialized' database in postgress as a layer in geoserver

    The datastore_expose_as_layer API action allows a user to publish a table as a layer in geoserver.
    It assumes the database table is already 'spacialized', i.e. has latitude and longitude columns 
    converted into a geographic shape.
    
    In order for the *expose* method to work, a unique key has to be defined via
    the datastore_create action. The available methods are:

    :param resource_id: resource id that the data is going to be stored under.
    :type resource_id: string
    
    **Results:**

    :returns: URI of the published layer.
    :rtype: string
    
    '''
    if 'id' in data_dict:
        data_dict['resource_id'] = data_dict['id']
    res_id = _get_or_bust(data_dict, 'resource_id')
    print ">>>>>>>>>>>>>>>>> working with: ",res_id
    
    cat = Catalog('http://localhost:8080/geoserver/rest')
    
    print ">>>>>>>>>>>>>>>>>>>>>> begin create workspace >>>>>>>>>>>>>>>>>>>>>>>>" 
    # reusing the existing one or create new workspace
    ngds_workspace = cat.get_workspace('NGDS')
    if ngds_workspace is None:    
        ngds_workspace = cat.create_workspace('NGDS', 'http://localhost:5000/ngds')
    print ">>>>>>>>>>>>>>>>>>>>>> end create workspace >>>>>>>>>>>>>>>>>>>>>>>>"
    
    print ">>>>>>>>>>>>>>>>>>>>>>  create store >>>>>>>>>>>>>>>>>>>>>>>>"
    #get existing or create new datastore
 
    # we utilize default values, instead of failing, if those parameters are not provided 
    if not 'geoserver' in data_dict:
        data_dict['geoserver'] = 'http://localhost:8080/geoserver/rest'
    if not  'workspace_name' in data_dict: 
        data_dict['workspace_name'] = 'NGDS'
    if not 'store_name' in data_dict:
        data_dict['store_name'] = 'datastore'
    if not 'pg_host' in data_dict:
        data_dict['pg_host'] = 'localhost'
    if not 'pg_port' in data_dict:
        data_dict['pg_port'] = '5432'
    if not 'pg_db' in data_dict:
        data_dict['pg_db'] = 'datastore'
    if not 'pg_user' in data_dict:
        data_dict['pg_user'] = 'ckanuser'
    if not 'pg_password' in data_dict:
        data_dict['pg_password'] = 'pass'
    if not 'db_type' in data_dict:
        data_dict['db_type'] = 'postgis'
    
    # tries to read existing datastore for the workspace, if the read is not
    # successful, crate the datastrore.
    try:
        store = cat.get_store('datastore', ngds_workspace)
        print ">>>>>>>>>>>>>>>>>>>> datastrore already exists >>>>>>>>>>>>>>>>"
    except Exception, ex:
        print ">>>>>>>>>>>>>>>>>>>> creating new datastrore info >>>>>>>>>>>>>>>>"
        geoserver_create_store(context, data_dict)
    
    print ">>>>>>>>>>>>>>>>>>>>>> start create layer >>>>>>>>>>>>>>>>>>>>>>>>"
    
    # we utilize the resource id as the layer name
    data_dict['layer_name'] = res_id
    geoserver_create_layer(context, data_dict)
    
    web_geoserver = data_dict['geoserver'].replace("rest", "web")
    web_url = web_geoserver+"?wicket:bookmarkablePage=:org.geoserver.web.data.resource.ResourceConfigurationPage&name="+res_id+"&wsName="+data_dict['workspace_name']
    
    
    return web_url

def datastore_remove_exposed_layer(context, data_dict):
    return


def datastore_list_exposed_layers(contect, data_dict):
    
    geoserver = _get_or_bust(data_dict, 'geoserver')
    cat = Catalog(geoserver)
    list_of_layers = cat.get_layers()
    
    return list_of_layers

    
def geoserver_create_workspace(context, data_dict):
    '''Create a workspace on the geoserver

    The geoserver_create_workspace API action allows a user to create a new workspace
    on a geoserver instance. 
    
    The available methods are:

    *create*
        It first checks if the workspace already exists. If it does not yet exist it
        is created.
        
    :param geoserver: url of the geoserver
    :type geoserver_url: string
    :param workspace_name: the name of the workspace that shall be created
    :type workspace_name: string
    :param workspace_uri: the URI of the workspace
    :type workspace_uri: string
    
    **Results:**

    :returns: The name of the workspace.
    :rtype: dictionary
    '''
    
    geoserver = _get_or_bust(data_dict, 'geoserver')
    workspace_name = _get_or_bust(data_dict, 'workspace_name')
    workspace_uri = _get_or_bust(data_dict, 'workspace_uri')

    cat = Catalog(geoserver)
    cat.create_workspace(workspace_name, workspace_uri)

def geoserver_delete_workspace(context, data_dict):
    '''Delete a workspace on a geoserver

    The geoserver_delete_workspace API action allows a user to delete a workspace
    on a geoserver instance. 
    
    The available methods are:

    *delete*
        It first checks if the workspace exists. If it does it gets deleted.
        
    :param geoserver: url of the geoserver
    :type geoserver_url: string
    :param workspace_name: the name of the workspace that shall be deleted
    :type workspace_name: string
    :param workspace_uri: the URI of the workspace
    :type workspace_uri: string
    
    **Results:**

    :returns: The name of the workspace.
    :rtype: dictionary
    '''
    
    geoserver = _get_or_bust(data_dict, 'geoserver')
    workspace_name = _get_or_bust(data_dict, 'workspace_name')
    # workspace_uri = _get_or_bust(data_dict, 'workspace_uri')

    cat = Catalog(geoserver)
    workspace= cat.get_workspace(workspace_name)
    cat.delete(workspace)


def geoserver_create_store(context, data_dict):
    '''Create a workspace on a geoserver

    The geoserver_create_store API action allows a user to create a new store
    on a geoserver instance. 
    
    The available methods are:

    *create*
        It first checks if the store already exists. If it does not yet exist it
        is created.
        
    :param geoserver: url of the geoserver
    :type geoserver_url: string
    :param workspace_name: the name of the workspace that shall hold the store
    :type workspace_name: string
    :param workspace_uri: the URI of the workspace
    :type workspace_uri: string
    :param store_name: the name of the store that shall be created
    :type store_name: string
    :param pg_host: the hostname of the postgres database; e.g. "localhost"
    :type pg_host: string
    :param pg_port: the hostname of the postgres database; e.g. 5432
    :type pg_port: integer
    :param pg_db: the name of the database; e.g. "datastore"
    :type pg_db: string
    :param pg_user: the user name to be used to access the database; e.g. "ckanuser"
    :type pg_user: string
    :param pg_password: the password to be used to access the database; e.g. "pass"
    :type pg_password: string
    :param db_type: the database type; e.g. "postgis"
    :type db_type: string
    
     
    
    **Results:**

    :returns: The name of the store.
    :rtype: dictionary
    '''
    print ">>>>>>>>>>>>>>>>>>>>>> geoserver_create_store reading parameters >>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    geoserver = _get_or_bust(data_dict, 'geoserver')
    workspace_name = _get_or_bust(data_dict, 'workspace_name')
    #workspace_uri = _get_or_bust(data_dict, 'workspace_uri')
    store_name =_get_or_bust(data_dict, 'store_name')
    pg_host= _get_or_bust(data_dict, 'pg_host')
    pg_port= _get_or_bust(data_dict, 'pg_port')
    pg_db= _get_or_bust(data_dict, 'pg_db')
    pg_user= _get_or_bust(data_dict, 'pg_user')
    pg_password= _get_or_bust(data_dict, 'pg_password')
    db_type= _get_or_bust(data_dict, 'db_type')

    print ">>>>>>>>>>>>>>>>>>>>>>> connecting to catalog at: "+geoserver
    cat = Catalog(geoserver)
    
    print ">>>>>>>>>>>>>>>>>>>>>> getting workspace >>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    print "workspace_name = ", workspace_name
    workspace= cat.get_workspace(workspace_name)
    
    print ">>>>>>>>>>>>>>>>>>>>>> create_datastore >>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    ds= cat.create_datastore(store_name, workspace)
    
    print ">>>>>>>>>>>>>>>>>>>>>> updating connection parameters >>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    print "password = ",pg_password
    ds.connection_parameters.update(host = pg_host,
                                    port = pg_port,
                                    database = pg_db,
                                    user = pg_user,
                                    password = pg_password,
                                    dbtype = db_type)

    cat.save(ds)
    
    # check if the store was created successfully
    ds = cat.get_store(store_name)
    ds.connection_parameters.update( user = pg_user, password = pg_password)
    
    return store_name


def geoserver_delete_store(context, data_dict):
    '''Delete a store on a geoserver

    The geoserver_delete_store API action allows a user to delete a store
    on a geoserver instance. 
    
    The available methods are:

    *delete*
        It first checks if the store exists. If it does it gets deleted.
        
    :param geoserver: url of the geoserver
    :type geoserver_url: string
    :param workspace_name: the name of the workspace containing the store that shall be deleted
    :type workspace_name: string
    :param workspace_uri: the URI of the workspace
    :type workspace_uri: string
    :param store_name: the name of the store that shall be deleted
    :type store_name: string
    
    
    **Results:**

    :returns: The name of the workspace.
    :rtype: dictionary
    '''
    
    geoserver = _get_or_bust(data_dict, 'geoserver')
    workspace_name = _get_or_bust(data_dict, 'workspace_name')
    workspace_uri = _get_or_bust(data_dict, 'workspace_uri')
    store_name = _get_or_bust(data_dict, 'workspace_uri')


    cat = Catalog(geoserver)
    store = cat.get_store(store_name, workspace_name)
    cat.delete(store)

def create_postgis_sql_layer(context, data_dict):
    '''Create a layer on geoserver through its restful API

    The create_postgis_sql_layer API action allows a user to create a layer in
    geoserver.
    
    The available methods are:

    *POST*
        It first creates then configures the layer.
        
    :param geoserver: url of the geoserver
    :type geoserver: string
    :param workspace_name: the name of the workspace containing the store that shall be deleted
    :type workspace_name: string
    :param layer_name: the name of the layer to be created
    :type layer_name: string
    :param resource_id: the name of the table to be published as a layer
    :type resource_id: string
    :param connection: a live database connectinon to the database containing the resouce_id table
    :type connection: database connection
    
    **Results:**

    :returns: The name of the layer.
    :rtype: dictionary
    '''
   
    workspace_name = _get_or_bust(data_dict, 'workspace_name')
    baseServerUrl = _get_or_bust(data_dict, 'geoserver')
    store_name =_get_or_bust(data_dict, 'store_name')
    resource_id = _get_or_bust(data_dict, 'resource_id')
    
    print ">>>>>>>>>>> connecting to database >>>>>>>>>>>>>"
    data_dict['connection_url'] = pylons.config['ckan.datastore.write_url']
    engine = db._get_engine(None, data_dict)
    context['connection'] = engine.connect()
    
    # 'layer_name', 'connection' and 'resource_id'
    # will be read by the SqlFeatureTypeDef
    
    if baseServerUrl is None:
        baseServerUrl="http://localhost:8080/geoserver/rest/"
    
    cat = Catalog(baseServerUrl)
    
    # builds the meta-data object used for the createion of the layer
    #print ">>>>>>>>>>>>>>>>> building definition >>>>>>>>>>>>>>>>"
    #definition = SqlFeatureTypeDef(context, data_dict)
    
    #print ">>>>>>>>>>>>>>>>> serializing definition >>>>>>>>>>>>>>>>"
    #print definition.serialize()
    
    
    #headers = { "Content-Type": "application/json" }
    
    print ">>>>>>>>>>>>>>>>> sending create layer POST >>>>>>>>>>>>>>>>"
    
    #headers, response = cat.http.request(featureType_url, "POST", definition.serialize(), headers)
    featureType_url = baseServerUrl + "/workspaces/" + workspace_name + "/datastores/"+store_name+"/featuretypes/"
    name= resource_id
    xml=  ("<featureType>"
       "<name>{name}</name>"
       "</featureType>").format(name=name)

    headers= {"Content-type": "text/xml"}

    headers, response = cat.http.request(featureType_url, "POST", xml, headers)
    
    print ">>>>>>>>>>>>>>>>> sent POST >>>>>>>>>>>>>>>>"
    assert 200 <= headers.status < 300, "Tried to create Geoserver layer but encountered a " + str(headers.status) + " error: " + response
    cat._cache.clear()

    return cat.get_layer(name)

    
def geoserver_create_layer(context, data_dict):
    '''Create a layer on a geoserver

    The geoserver_create_layer API action allows a user to create a new layer
    on a geoserver instance. 
    
    The available methods are:

    *create*
        It first checks if the layer already exists. If it does not yet exist it
        is created.
        
    :param geoserver: url of the geoserver
    :type geoserver_url: string
    :param workspace_name: the name of the workspace that shall hold the store
    :type workspace_name: string
    :param workspace_uri: the URI of the workspace
    :type workspace_uri: string
    :param store_name: the name of the store that shall be created
    :type store_name: string
    :param pg_host: the hostname of the postgres database; e.g. "localhost"
    :type pg_host: string
    :param pg_port: the hostname of the postgres database; e.g. 5432
    :type pg_port: integer
    :param pg_db: the name of the database; e.g. "datastore"
    :type pg_db: string
    :param pg_user: the user name to be used to access the database; e.g. "ckanuser"
    :type pg_user: string
    :param pg_password: the password to be used to access the database; e.g. "pass"
    :type pg_password: string
    :param db_type: the database type; e.g. "postgis"
    :type db_type: string
    
    :param layer_name: the name of the layer that shall be created
     
    
    **Results:**

    :returns: The name of the store.
    :rtype: dictionary
    '''
    print ">>>>>>>>>>>>>>>>>>>>>> start create layer >>>>>>>>>>>>>>>>>>>>>>>>"
    
    geoserver = _get_or_bust(data_dict, 'geoserver')
    workspace_name = _get_or_bust(data_dict, 'workspace_name')
    #workspace_uri = _get_or_bust(data_dict, 'workspace_uri')
    store_name =_get_or_bust(data_dict, 'store_name')
    pg_host= _get_or_bust(data_dict, 'pg_host')
    pg_port= _get_or_bust(data_dict, 'pg_port')
    pg_db= _get_or_bust(data_dict, 'pg_db')
    pg_user= _get_or_bust(data_dict, 'pg_user')
    pg_password= _get_or_bust(data_dict, 'pg_password')
    db_type= _get_or_bust(data_dict, 'db_type')

    layer_name= _get_or_bust(data_dict, 'layer_name')

    print ">>>>>>>>>>>>>>>>>>>> connecting to catalog: "+geoserver
    cat = Catalog(geoserver)
    #print ">>>>>>>>>>>>>>>>>>>> connecting to workspace: "+workspace_name
    #workspace= cat.get_workspace(workspace_name)
    #ds = cat.get_store(store_name)
    
    print ">>>>>>>>>>>>>>>>>>>> check if layer exists >>>>>>>>>>>>>>>>>>>>"
    if cat.get_layer(layer_name) is None:
        print ">>>>>>>>>>>>>>>>>>>> create new layer object >>>>>>>>>>>>>>>>>>>>"
        create_postgis_sql_layer(context, data_dict)
    else:
        print ">>>>>>>>>>>>>>>>>>>> layer already exists >>>>>>>>>>>>>>>>>>>>"
    
    return
    
    

