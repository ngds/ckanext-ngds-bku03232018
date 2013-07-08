from solr import SolrConnection
import solr as solr

class NgdsSolrConnection(SolrConnection):

    @solr.core.committing
    def update_fields(self, docs, fields_to_update, commit=False):
        lst = [u'<add>']
        #for doc in docs:
        self.__add_update_fields(lst, docs, fields_to_update)
        lst.append(u'</add>')
        return ''.join(lst)

    def __add_update_fields(self, lst, fields, fields_to_update):
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


        try:
            request = '-F file=@%s' % file_path
            selector = '%s/update/extract?extractOnly=true&extractFormat=text ' % self.path
            _headers = self.auth_headers.copy()
            self.conn.request('POST', selector, request, _headers)
            rsp = solr.core.check_response_status(self.conn.getresponse())
            data = rsp.read()
        finally:
            if not self.persistent:
                self.close()

        # Detect old-style error response (HTTP response code
        # of 200 with a non-zero status).
        starts = data.startswith
        if starts('<result status="') and not starts('<result status="0"'):
            from xml.dom.minidom import parseString
            from solr.core import SolrException

            data = self.decoder(data)[0]
            parsed = parseString(data)
            status = parsed.documentElement.getAttribute('status')
            if status != 0:
                reason = parsed.documentElement.firstChild.nodeValue
                raise SolrException(rsp.status, reason)
        return data

def make_connection():

    from ckan.lib.search.common import SolrSettings

    solr_url, solr_user, solr_password = SolrSettings.get()
    assert solr_url is not None
    if solr_user is not None and solr_password is not None:
        return NgdsSolrConnection(solr_url, http_user=solr_user,
                              http_pass=solr_password)
    else:
        return NgdsSolrConnection(solr_url)