from osgeo import ogr
from osgeo import osr
import zipfile
from os import path, environ, pathsep
from re import search
from ckanext.ngds.ngdsui.misc.helpers import file_path_from_url
from pylons import config
from ckan.plugins import toolkit
import subprocess

class Shapefile:
    resource = {}
    file_path = ""
    is_valid = False
    unzipped_dir = None
    ogr_source = {
        "driver": None,
        "source": None,
        "layer": None,
        "srs": None
    }
    ogr_destination = {
        "driver": None,
        "source": None,
        "layer": None,
        "srs": None
    }

    def __init__(self, resource_id=""):
        # Get the resource
        self.resource = toolkit.get_action("resource_show")(None, {"id": resource_id})
        
        # Get the path to the file
        url = self.resource["url"]
        self.file_path = file_path_from_url(url)
        
        # Check that it is a valid zip file
        self.is_valid = self.validate()

    def validate(self):
        """Make sure that the uploaded zip file is a valid shapefile"""        
        # Check that it is a zip file
        if zipfile.is_zipfile(self.file_path):
            # Open the zipfile as read-only
            with zipfile.ZipFile(self.file_path) as zf:
                required = [".shp", ".shx", ".dbf"]
                optional = [".prj", ".sbn", ".sbx", ".fbn", ".fbx", ".ain", ".aih", ".ixs", ".mxs", ".atx", ".cpg", ".xml"]
                
                # Look at the file extensions in the zipfile
                extensions = [path.splitext(info.filename)[1] for info in zf.infolist()]
                
                # Check that all the required extensions are there
                if len([ext for ext in required if ext in extensions]) == len(required):
                    # Check that there are not extension in there that are not required
                    if len([ext for ext in extensions if ext in optional]) == len(extensions) - len(required):
                        return True
                        '''# If we can make a OGR Shapefile datasource, then we are valid
                        try:
                            obj = self.get_source_layer()
                            if obj:
                                return True
                        except Exception as ex:                                                    
                            pass'''

        raise Exception("Not a valid shapefile")

    def unzip(self):
        """Unzip the shapefile into a pre-determined directory next to it"""
        # Generate the path for the directory to be unzipped to
        unzipped_dir = self.file_path[:-4] + "_UNZIPPED"
        
        # Open the zipfile and extract everything (overwrite if there's stuff there??)
        with zipfile.ZipFile(self.file_path) as zf:
            zf.extractall(unzipped_dir)
        
        # Return the path to the unzipped directory
        return unzipped_dir
    
    def get_source_layer(self):
        """Get a OGRLayer for this shapefile"""
        # Where is the unzipped shapefile?
        if self.unzipped_dir is None:
            self.unzipped_dir = self.unzip()

        # Generate the OGR DataSource
        input_driver = ogr.GetDriverByName("ESRI Shapefile")
        input_datasource = input_driver.Open(self.unzipped_dir, 0)
        
        # A dataSource is always an array, but shapefiles are always by themselves. Get the layer
        layer = input_datasource.GetLayerByIndex(0)

        # Cache the OGR objects so they don't get cleaned up
        self.ogr_source["driver"] = input_driver
        self.ogr_source["source"] = input_datasource
        self.ogr_source["layer"] = layer

        return layer

    def get_destination_source(self):
        """Get an OGRDataSource for the default PostgreSQL destination"""
        # Generate connection details from CKAN config
        datastore_url = config.get("ckan.datastore.write_url")
        pattern = "://(?P<user>.+?):(?P<password>.+?)@(?P<host>.+?)/(?P<dbname>.+)$"
        params = search(pattern, datastore_url)
        connection = (
            params.group("host"),
            params.group("dbname"),
            params.group("user"),
            params.group("password")
        )
        ogr_connection_string = "PG: host=%s port=5432 dbname=%s user=%s password=%s" % connection
        
        # Generate the destination DataSource
        try:
            output_driver = ogr.GetDriverByName("PostgreSQL")
            destination_layer = output_driver.Open(ogr_connection_string)

            # Cache the OGR objects so they don't get cleaned up
            self.ogr_destination["driver"] = output_driver
            self.ogr_destination["layer"] = destination_layer

            return destination_layer
        except Exception as ex:
            return None

    def create_destination_layer(self, destination_source, name, epsg=4326):
        """Create a table in the given destination OGRDataSource"""
        # Get the shapefile OGR Layer and its "definition"
        source = self.get_source_layer()
        source_def = source.GetLayerDefn()
        
        # Read some shapefile properties
        geom_type = ogr.wkbUnknown
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(epsg)

        # Cache the OGR objects so they don't get cleaned up
        self.ogr_source["srs"] = srs
        
        # Create the destination layer in memory
        new_layer = destination_source.CreateLayer(name, srs, geom_type, ["OVERWRITE=YES"])
        
        # Iterate through shapefile fields, add them to the new layer
        for i in range(source_def.GetFieldCount()):
            field_def = source_def.GetFieldDefn(i)
            new_layer.CreateField(field_def)
        
        # Commit it
        new_layer.CommitTransaction()

        # Cache the OGR objects so they don't get cleaned up
        self.ogr_destination["layer"] = new_layer

        return True
        
    def get_destination_layer(self, destination_source, name):
        """Given an OGRDataSource (destination_source), find an OGRLayer within it by name"""
        layer = destination_source.GetLayerByName(name)

        # Cache the OGR objects so they don't get cleaned up
        self.ogr_destination["layer"] = layer

        return layer
    
    def publish(self, destination_layer):
        """Move shapefile data into the given destination OGRLayer"""
        # Get information about the destination layer
        dest_def = destination_layer.GetLayerDefn()
        target_srs = destination_layer.GetSpatialRef()
        #target_srs = dest_def.GetSpatialRef()

        # Cache the OGR objects so they don't get cleaned up
        self.ogr_destination["srs"] = target_srs
        
        # Setup the coordinate transformation
        source = self.get_source_layer()
        source_srs = source.GetSpatialRef()
        transformation = osr.CoordinateTransformation(source_srs, target_srs)

        # Iterate through the shapefile features. Project each one and add it to the destination
        source_record = source.GetNextFeature()
        while source_record is not None:            
            # Create a new, blank feature in the destination layer
            dest_record = ogr.Feature(dest_def)
            
            # Set its geometry
            #new_geom = self.reproject(source_record, target_srs)
            geom = source_record.GetGeometryRef()
            geom.Transform(transformation)
            dest_record.SetGeometry(geom)
            
            # Set its attributes from the source feature
            dest_record.SetFrom(source_record)
            
            # Save it to the destination layer and iterate
            destination_layer.CreateFeature(dest_record)
            source_record = source.GetNextFeature()
        
    def reproject(self, feature, target_srs):
        """Reproject a single feature's geometry into a new SRS and return the new geometry"""
        # Get the appropriate transformations and build a reprojected geometry
        source_srs = self.ogr_source["layer"].GetSpatialRef()
        transformation = osr.CoordinateTransformation(source_srs, target_srs)

        # Cache the OGR objects so they don't get cleaned up
        self.ogr_source["srs"] = source_srs
        self.transformation = transformation

        return feature.GetGeometryRef().Transform(transformation)

    def get_name(self):
        if self.unzipped_dir is None:
            self.unzipped_dir = self.unzip()

        # Generate the OGR DataSource
        inputDriver = ogr.GetDriverByName("ESRI Shapefile")
        dataSource = inputDriver.Open(self.unzipped_dir, 0)

        # A dataSource is always an array, but shapefiles are always by themselves. Get the layer
        return dataSource.GetLayerByIndex(0).GetName()

    def default_publish(self):
        datastore_url = config.get("ckan.datastore.write_url")
        pattern = "://(?P<user>.+?):(?P<password>.+?)@(?P<host>.+?)/(?P<dbname>.+)$"
        params = search(pattern, datastore_url)
        connection = (
            params.group("host"),
            params.group("dbname"),
            params.group("user"),
            params.group("password")
        )
        ogr_connection_string = "PG: host=%s port=5432 dbname=%s user=%s password=%s" % connection
        name = self.get_name()

        self.publish_as_subprocess("PostgreSQL", ogr_connection_string, name, name, 4326)

    def publish_as_subprocess(self, destination_driver, destination_connection, destination_name, shapefile_name, epsg):
        def find_ogr2ogr():
            paths = environ["PATH"].split(pathsep)
            paths.append("/usr/local/bin")
            for p in paths:
                path_dir = p.strip('"')
                exe = path.join(path_dir, "ogr2ogr")
                if path.exists(exe):
                    return exe
            return None

        ogr2ogr = find_ogr2ogr()
        if not ogr2ogr:
            raise Exception("Could not find ogr2ogr")

        parameters = [
            ogr2ogr,
            "-f",
            destination_driver,
            "-t_srs",
            "EPSG:%i" % epsg,
            "-nln",
            "%s" % destination_name,
            destination_connection,
            path.join(self.unzipped_dir, "%s.shp" % shapefile_name)
        ]

        e = environ
        p = subprocess.Popen(parameters)
        print "worked?"