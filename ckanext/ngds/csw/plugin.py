from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer, IRoutes
from ckanext.ngds.csw.model.csw_records import define_tables
from ckanext.ngds.csw.iso_support import add_csw_model

class CswPlugin(SingletonPlugin):
    """The purpose of this plugin is to add CSW support"""
    
    implements(IConfigurer) # Allows access to configurations (like template locations)
    
    def update_config(self, config):
        """IConfigurable function. config is a dictionary of configuration parameters"""
        # Provides a point to do mappings from classes to database tables whenever CKAN is run
        define_tables()
        
        # Add CswPackage class for conversion to/from ISO19139 XML
        add_csw_model()
        
    implements(IRoutes) # Allows me to add URLs to the CKAN site
    
    def before_map(self, map):
        """
        Called before the routes map is generated. ``before_map`` is before any
        other mappings are created so can override all other mappings.
    
        :param map: Routes map object
        :returns: Modified version of the map object
        """
        
        # Identify the controller class for the new route
        controller = "ckanext.ngds.csw.csw_wrapper:CswController"
        
        # Now build a route
        #   ``action`` is the method to call on the controller class
        #   ``conditions`` seem to apply conditions to the route. I don't know the limitations...
        map.connect('csw-server',
                    '/csw',
                    controller=controller,
                    action="csw",
                    conditions={"method": ["GET", "POST"]})
        
        # Test the ISO XML output
        map.connect('iso-test',
                    '/iso-test/:package_id',
                    controller=controller,
                    action="xml_test")
        
        return map
    
    def after_map(self, map):
        """
        Called after routes map is set up. ``after_map`` can be used to
        add fall-back handlers.
    
        :param map: Routes map object
        :returns: Modified version of the map object
        """
        return map