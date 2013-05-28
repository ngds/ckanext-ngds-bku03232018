from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer, IRoutes, IDomainObjectModification, IActions
from ckan.model.domain_object import DomainObjectOperation
from ckanext.ngds.csw.logic import view, pycsw
from ckanext.ngds.csw.model.csw_records import define_tables
from ckan.model import meta
from ckan.plugins import toolkit


class CswPlugin(SingletonPlugin):
    """The purpose of this plugin is to add CSW support"""
    
    implements(IConfigurer) # Allows access to configurations (like template locations)
    
    def update_config(self, config):
        """IConfigurable function. config is a dictionary of configuration parameters"""
        # Provides a point to do mappings from classes to database tables whenever CKAN is run
        define_tables()
        toolkit.add_template_directory(config, "templates")

    implements(IRoutes) # Allows me to add URLs to the CKAN site
    
    def before_map(self, map):
        """
        Called before the routes map is generated. ``before_map`` is before any
        other mappings are created so can override all other mappings.
    
        :param map: Routes map object
        :returns: Modified version of the map object
        """

        # Now build a route
        #   ``action`` is the method to call on the controller class
        #   ``conditions`` seem to apply conditions to the route. I don't know the limitations...
        map.connect('csw-server',
                    '/csw',
                    controller="ckanext.ngds.csw.csw_wrapper:CswController",
                    action="csw",
                    conditions={"method": ["GET", "POST"]})


        map.connect("serialize-record",
                    "/serialize/:package_id/:format",
                    controller="ckanext.ngds.csw.controllers.serializer:PackageSerializer",
                    action="dispatch",
                    conditions={"method": ["GET"]})

        # Test the ISO XML output
        map.connect('iso-test',
                    '/iso-test/:package_id',
                    controller="ckanext.ngds.csw.csw_wrapper:CswController",
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

    """
    implements(IDomainObjectModification)
    
    def notify(self, entity, operation):

        The goal here is to change the pycsw table when CKAN info is changed.
        
        I think I'll need to listen for changes to ckan.model.Package and ckanext.ngds.metadata.model.ResponsibleParty
        
        Will be tricky to find all the packages that implement a given ResponsibleParty and update them


        from ckan.model import Package
        from ckanext.ngds.metadata.model.additional_metadata import ResponsibleParty
        from ckanext.ngds.csw.model.csw_records import CswRecord
        from ckan.plugins import toolkit

        # package is in draft mode until you complete the entire set of forms
        if isinstance(entity, Package) and entity.state != "draft":
            # action package_delete only changes the package state to deleted
            if operation == DomainObjectOperation.changed and entity.state == "deleted":
                meta.Session.query(CswRecord).filter_by(package_id=entity.id).delete()

            # This would be new or changed packages
            elif operation != DomainObjectOperation.deleted:
                toolkit.get_action("metadata_to_pycsw")(None, {"id": entity.id})

            # I don't know how to cause this, I assume it would be some kind of full delete of the package
            else:
                meta.Session.query(CswRecord).filter_by(package_id=entity.id).delete()
            
        elif isinstance(entity, ResponsibleParty):
            pass
    """

    implements(IActions)

    def get_actions(self):
        return {
            "iso_metadata": view.iso_metadata,
            "metadata_to_pycsw": pycsw.metadata_to_pycsw,
            "full_sync": pycsw.full_sync
        }