import ogr
import osr
from ckanext.ngds.geoserver.model.Data import Data
from ckan.plugins import toolkit
#from ckan.model.resource import Resource

class Shapefile(Data):
    resource = None

    def __init__(self, resource_id):
        self.resource = toolkit.get_action("resource_show")(None, {"id": resource_id})
        self.zip_file = ""
        pass

    def unzip(self):
        if (zipfile.is_zipfile(inputZip)):
            self.zipfile = inputZip
            print "Path is a .zip directory."
        else:
            print "ERROR: Not a .zip file"
            sys.exit(1)

        valid = []
        invalid = []
        validMandatory = [".shp",".shx",".dbf"]
        validOptional = [".prj",".sbn",".sbx",".fbn",".fbx",".ain",".aih",".ixs",".mxs",".atx",".cpg"]
        with zipfile.ZipFile(self.zipfile) as zf:
            for info in zf.infolist():
                f = info.filename
                if os.path.splitext(f)[1] in validMandatory:
                    valid.append(f)
                    pass
                elif os.path.splitext(f)[1] in validOptional:
                    pass
                elif f.endswith(".shp.xml"):
                    pass
                else:
                    invalid.append(f)
            if len(valid) != 3:
                print "ERROR: Missing a required filetype ('.shp', '.shx', '.dbf')-- ABORTING"
                sys.exit(1)
            if len(invalid) != 0:
                print "ERROR: One or more invalid filetype(s) were found in .zip directory-- ABORTING"
                sys.exit(1)
            else:
                print "Shapefile is a valid dataset."
        del valid, invalid, validMandatory, validOptional

        unZippedDir = self.zipfile[:-4]+"_UNZIPPED"
        with zipfile.ZipFile(self.zipfile) as zf:
            print "Extracting .zip directory"
            zf.extractall(unZippedDir)
            print "Completed extracting .zip directory"

        pass

    def reproject(self):
        inputDriver = ogr.GetDriverByName("ESRI Shapefile")
        dataSource = inputDriver.Open(self.shapefile, 0)
        sourceLayer = dataSource.GetLayerByIndex(0)
        srs = sourceLayer.GetSpatialRef()
        pass

    def validate(self):
        pass

    def publish(self):
        pass

    def unpublish(self):
        pass