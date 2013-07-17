import logging

from ckan.lib.search.common import SearchIndexError
from paste.deploy.converters import asbool
from pylons import config as ckan_config

from ckanext.ngds.lib.common import make_connection


log = logging.getLogger(__name__)

class FullTextIndexer:

    def __init__(self):
        pass

    def index_resource_file(self, data_dict, file_index_field, file_path, defer_commit=False):
        """

        :param data_dict:
        :param file_path:
        :return:
        """

        try:
            conn = make_connection()
            #commit = not defer_commit

            if not asbool(ckan_config.get('ckan.search.solr_commit', 'true')):
                commit = False
            commit = True
            query = "%s:%s" % ('id',data_dict['id'])

            response = conn.query(query)

            results = response.results

            if results and len(results) > 0:

                index_id = results[0]['index_id']

                print "index_id: ", index_id

                file_content = conn._extract_content(file_path)

                data_dict[file_index_field] = file_content
                data_dict['index_id']=index_id

                conn.update_fields(data_dict, [file_index_field], commit=commit)
        except Exception, e:
            log.exception(e)
            raise SearchIndexError(e)
        finally:
            conn.close()