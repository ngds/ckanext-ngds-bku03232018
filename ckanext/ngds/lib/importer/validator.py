import ckanext.ngds.lib.importer.helper as import_helper
import ckanext.ngds.lib.importer.importer as ngds_importer

#Need to decide our own Read only keys
readonly_keys = ('id', 'revision_id',
                 'relationships',
                 'license',
                 'ratings_average', 'ratings_count',
                 'ckan_url',
                 'metadata_modified',
                 'metadata_created',
                 'notes_rendered')
referenced_keys = ('category','status','topic','protocol')

class NGDSValidator(object):

    def __init__(self,data_file,resource_path):
        self._data_file = data_file
        self._resource_path = resource_path

    @classmethod
    def validate(self):
        """
        This method will validate the give data file and the resoureces.If the validation is successfull then returns Status as "VALID" 
        otherwise returns the status as "INVALID" and validaiton message.
        """        
       
        package_import = ngds_importer.NGDSPackageImporter(filepath=file_path)