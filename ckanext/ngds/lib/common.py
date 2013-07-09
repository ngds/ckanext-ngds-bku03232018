from solr import SolrConnection
import solr as solr

class NgdsSolrConnection(SolrConnection):

    @solr.core.committing
    def update_fields(self, docs, fields_to_update, commit=False):
        """

        """
        lst = [u'<add>']
        #for doc in docs:
        self.__add_update_fields(lst, docs, fields_to_update)
        lst.append(u'</add>')
        xml_content = ''.join(lst)
        return xml_content

    def __add_update_fields(self, lst, fields, fields_to_update):
        """

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
            print "exception while extracting the file contents."
            raise ex

        return data

def check_response_status(response):
    """

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

    """

    from ckan.lib.search.common import SolrSettings

    solr_url, solr_user, solr_password = SolrSettings.get()
    assert solr_url is not None
    if solr_user is not None and solr_password is not None:
        return NgdsSolrConnection(solr_url, http_user=solr_user,
                              http_pass=solr_password)
    else:
        return NgdsSolrConnection(solr_url)