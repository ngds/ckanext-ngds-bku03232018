"""
This file contains the core functions to do the full-text Indexing of a document uploaded as part of Resource.
"""
import logging

from ckan.lib.search.common import SearchIndexError
from paste.deploy.converters import asbool
from pylons import config as ckan_config

#from ckanext.ngds.lib.common import make_connection


log = logging.getLogger(__name__)

class FullTextIndexer:

    def __init__(self):
        pass

    def index_resource_file(self, data_dict, file_index_field, file_path, defer_commit=False):
        """
        Full text indexes the input file along with the package. So that any text search matching content in the file
        will return the package. Index ID of the package is retrieved from Solr and file content to be indexed is
        extracted using Solr and appended to the data_dictionary and updated in Solr. Current version of Solr doesn't
        support updating a particualr field of an index, thats why the entire package content is passed again for
        indexing.

        :param data_dict: Data dictionary of the package which contains the file as part of one of its resources
        :param file_index_field: Holds the extracted content of file in the Indexed dictionary.
        :param file_path: Actual file path
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

                file_content = conn._extract_content(file_path)

                data_dict[file_index_field] = file_content
                data_dict['index_id']=index_id

                conn.update_fields(data_dict, [file_index_field], commit=commit)
        except Exception, e:
            log.exception(e)
            raise SearchIndexError(e)
        finally:
            conn.close()


from solr import SolrConnection
import solr as solr

class NgdsSolrConnection(SolrConnection):
    """
    Extends the SolrConnection to support document extraction process in addition to the existing functions.
    """

    @solr.core.committing
    def update_fields(self, docs, fields_to_update, commit=False):
        """
        Add several documents to the Solr server.

        `docs`
            An iterable of document dictionaries.

        Supports commit-control arguments.
        """
        lst = [u'<add>']
        #for doc in docs:
        self.__add_update_fields(lst, docs, fields_to_update)
        lst.append(u'</add>')
        xml_content = ''.join(lst)
        return xml_content

    def __add_update_fields(self, lst, fields, fields_to_update):
        """
        Iterates through the list of dictionary fields to construct XML document for indexing in Solr.
        Does some basic data conversions like date to String, Boolean to String for Solr system to understand the values
        If a field is marked as to be updated then 'update' flag is set for Solr to update the existing field. Otherwise
         new key is created in Solr Index.
        """
        from xml.sax.saxutils import escape, quoteattr
        import datetime
        lst.append(u'<doc>')
        for field, value in fields.items():
            # Handle multi-valued fields if values
            # is passed in as a list/tuple
            if not isinstance(value, (list, tuple, set)):
                values = [value]
            else:
                values = value

            for value in values:
                # ignore values that are not defined
                if value == None:
                    continue
                # Do some basic data conversion
                if isinstance(value, datetime.datetime):
                    value = solr.core.utc_to_string(value)
                elif isinstance(value, datetime.date):
                    value = datetime.datetime.combine(
                        value, datetime.time(tzinfo=solr.core.UTC()))
                    value = solr.core.utc_to_string(value)
                elif isinstance(value, bool):
                    value = value and 'true' or 'false'
                if fields_to_update and field in fields_to_update:
                    lst.append('<field name=%s update="set">%s</field>' % ((quoteattr(field),escape(unicode(value)))))
                else:
                    lst.append('<field name=%s>%s</field>' % ((quoteattr(field), escape(unicode(value)))))
        lst.append('</doc>')

    def _extract_content(self, file_path):
        """
        Extracts the content of the file for the indexing. This supports all the file formats supported by Tika(used
        by Solr). Receives the response in XML format from Solr and the actual file content is extracted out of it and
        returned.
        """

        try:
            selector = '%s/update/extract?extractOnly=true&extractFormat=xml ' % self.url
            _headers = self.auth_headers.copy()

            import requests
            files = {'file': open(file_path, 'rb')}
            response = requests.post(selector, files=files, headers=_headers)
            check_response_status(response)

            from lxml import etree

            response_text = response.text

            response_text = response_text.encode("UTF-8")

            root = etree.fromstring(response_text)

            expr = "//str[@name = $name]"

            file_content = root.xpath(expr, name=file_path)

            data = None

            if file_content and len(file_content) > 0:
                data = file_content[0].text

        except Exception, ex:
            log.exception(ex)
            log.erro("exception while extracting the file contents.")
            raise ex

        return data

def check_response_status(response):
    """
    If the response code is not 200 (Success) then raises the SolrException with response message.
    """
    if response.status_code != 200:
        ex = solr.SolrException(response.status_code, response.reason)
        try:
            ex.body = response.read()
        except:
            pass
        raise ex
    return response

def make_connection():
    """
    Creates NGDS Solr Connection based on the values configured in pylons configuration file.
    """

    from ckan.lib.search.common import SolrSettings

    solr_url, solr_user, solr_password = SolrSettings.get()
    assert solr_url is not None
    if solr_user is not None and solr_password is not None:
        return NgdsSolrConnection(solr_url, http_user=solr_user,
                              http_pass=solr_password)
    else:
        return NgdsSolrConnection(solr_url)