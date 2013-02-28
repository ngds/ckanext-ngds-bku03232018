from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer, IRoutes, IDomainObjectModification
from ckan.model.domain_object import DomainObjectOperation

from ckanext.ngds.csw.model.csw_records import define_tables
from ckan.model import meta

class CswPlugin(SingletonPlugin):
    """The purpose of this plugin is to add CSW support"""
    
    implements(IConfigurer) # Allows access to configurations (like template locations)
    
    def update_config(self, config):
        """IConfigurable function. config is a dictionary of configuration parameters"""
        # Provides a point to do mappings from classes to database tables whenever CKAN is run
        define_tables()    
        
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
    
    implements(IDomainObjectModification)
    
    def notify(self, entity, operation):
        """
        The goal here is to change the pycsw table when CKAN info is changed.
        
        I think I'll need to listen for changes to ckan.model.Package and ckanext.ngds.metadata.model.ResponsibleParty
        
        Will be tricky to find all the packages that implement a given ResponsibleParty and update them
        
        I'm not sure what all the operations will be, either
        [ new, changed, deleted ]
        """
        from ckan.model import Package
        from ckanext.ngds.metadata.model.additional_metadata import ResponsibleParty
        from ckanext.ngds.metadata.model.iso_package import IsoPackage
        from ckanext.ngds.csw.model.csw_records import CswRecord
        
        if isinstance(entity, Package):
            iso = IsoPackage(entity)
            csw = CswRecord.from_iso_package(iso)
            csw = meta.Session.merge(csw)
            
            if operation != DomainObjectOperation.deleted:
                meta.Session.add(csw)
            else:
                csw.delete()
            
        elif isinstance(entity, ResponsibleParty):
            pass
        