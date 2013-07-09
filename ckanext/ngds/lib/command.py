from ckan.lib.cli import CkanCommand
from ckanext.ngds.lib.importer.importer import BulkUploader

class APICommand(CkanCommand):
    """
    Performs paster commands
    """
    summary = "General Command"
    usage = __doc__
    max_args = 4
    min_args = 0
    
    def command(self):
        self._load_config()
        cmd = self.args[0]
        #print "Arguments: ",self.args
        if cmd == "import":
            #print "File Path: ",self.args[1]
            bulkLoader = BulkUploader()
            #bulkLoader.importpackagedata(file_path=self.args[1],resource_dir=self.args[2])
            bulkLoader.execute_bulk_upload()
        else:
            from ckanext.ngds.lib.index import FullTextIndexer

            text_indexer = FullTextIndexer()
            data_dict = {'id' : 'e6218c2c-342e-4834-9945-f2c64ff24d45',
                       'site_id' : 'default'}
            field_to_add = 'resource_file_%s' % '5ffecb7c-1b0c-42df-bbff-75bd6631c31f'
            file_path = '/home/ngds/Downloads/CDG_USA_HostIB.pdf'
            text_indexer.index_resource_file(data_dict,'resource_file_b15829ec-2a0a-48e3-a442-ba5a32b0f8e0', file_path, defer_commit=True)

