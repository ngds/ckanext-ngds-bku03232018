"""
Thanks to OpenDataCatalog for inspiration and guidance on how to wrap pycsw
into a python function.
https://github.com/azavea/Open-Data-Catalog
"""

import os.path
from ConfigParser import SafeConfigParser
from ckan.lib.base import BaseController

from pycsw import server

# Configuration parameters required for pycsw server. 
#    Especially the metadata:main section should be end-user configurable
CONFIGURATION = {
    'server': {
        'home': '.',
        'mimetype': 'application/xml; charset=UTF-8',
        'encoding': 'UTF-8',
        'language': 'en-US',
        'maxrecords': '10',
        'profiles': 'apiso,dif,fgdc,atom,ebrim',
    },
    'repository': {
        'database': 'postgresql://ckanuser:secret@localhost:5432/ckan', # read from configuration
        'table': 'csw_record'
    },
    'metadata:main': { # Read all from configuration
        'identification_title': 'NGDS CSW',
        'identification_abstract': 'NGDS is awesome',
        'identification_keywords': 'ngds,csw,ogc,catalog',
        'identification_keywords_type': 'theme',
        'identification_fees': 'None',
        'identification_accessconstraints': 'None',
        'provider_name': 'Roger Mebowitz',
        'provider_url': 'http://geothermaldatasystem.org',
        'contact_name': 'Roger Mebowitz',
        'contact_position': 'Roger Mebowitz',
        'contact_address': '416 W. Congress St. Ste. 100',
        'contact_city': 'Tucson',
        'contact_stateorprovince': 'Arizona',
        'contact_postalcode': '85701',
        'contact_country': 'United States of America',
        'contact_phone': '+01-xxx-xxx-xxxx',
        'contact_fax': '+01-xxx-xxx-xxxx',
        'contact_email': 'Roger Mebowitz',
        'contact_url': 'http://geothermaldatasystem.org',
        'contact_hours': '0800h - 1600h EST',
        'contact_instructions': 'During hours of service.  Off on weekends.',
        'contact_role': 'pointOfContact',
    },
    'metadata:inspire': { # from configuration
        'enabled': 'false',
        'languages_supported': 'eng',
        'default_language': 'eng',
        'date': '2012-06-11',
        'gemet_keywords': 'Utility and governmental services',
        'conformity_service': 'notEvaluated',
        'contact_name': 'Roger Mebowitz',
        'contact_email': 'Roger Mebowitz',
        'temp_extent': '2012-06-11/2012-06-11',
    }
}

class CswController(BaseController):    
    def csw(self, *args, **kwargs):
        """Wrapper around pycsw for dispatching CSW requests"""        
        
        # Cycle through the CONFIGURATION dictionary and push the params into the config object
        config = SafeConfigParser()
        for section, options in CONFIGURATION.iteritems():
            config.add_section(section)
            for k, v in options.iteritems():
                config.set(section, k, v)
    
        # Calculate and insert the server URL into the config
        server_url = 'http://%s%s' % \
            (kwargs["environ"]['HTTP_HOST'],
             kwargs["environ"]['PATH_INFO'])    
        config.set('server', 'url', server_url)

        # Make a copy of the WSGI request environment and add parameters
        env = kwargs["environ"].copy()
                
        query = kwargs["environ"]["QUERY_STRING"]
        if query != "":
            absolute_uri = "%s?%s" % (server_url, query)
        else:
            absolute_uri = server_url
            
        env.update({ 
            'local.app_root': os.path.dirname(__file__),                
            'REQUEST_URI': absolute_uri
        })
        
        # Create an instance of pycsw's CSW class to handle the request 
        csw = server.Csw(config, env)
    
        # Run the request
        content = csw.dispatch_wsgi()
        
        # Set the response Content-type, and return the result
        kwargs["pylons"].response.content_type = csw.contenttype       
        return content
    
    def xml_test(self, *args, **kwargs):
        from ckan import model
        '''test_package = model.Package.get(kwargs["package_id"])
        test_csw_package = model.IsoPackage(test_package)        
        kwargs["pylons"].response.content_type = "text/xml"
        return test_csw_package.to_iso_xml()'''
        node = model.HarvestNode("http://debug.catalog.usgin.org/geoportal/csw")
        node.do_harvest()