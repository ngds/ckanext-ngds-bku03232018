import ckan.plugins as p
import ckan.model as model

class NGDSClient(p.SingletonPlugin):


    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IRoutes, inherit=True)

    """
    p.implements(p.ITemplateHelpers)
    p.implements(p.IActions)
    p.implements(p.IAuthFunctions)
    p.implements(p.IFacets)
    p.implements(p.IPackageController)
    p.implements(p.IDatasetForm)
    """

    def update_config(self, config):
        """
        Extends 'update_config' function in IConfigurer object.  Registers the
        templates and static files directories with CKAN.

        @config: Pylons global config object
        """
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_public_directory(config, 'public')

    def get_helpers(self):
        pass

    def before_map(self, map):
        controller = 'ckanext.ngds.client.controllers.view:ViewController'
        map.connect('map_search', '/map_search', controller=controller,
                    action='render_map_search')
        map.connect('library_search', '/library_search', controller=controller,
                    action='render_library_search')
        map.connect('resources', '/resources', controller=controller,
                    action='render_resources')
        map.connect('contribute', '/contribute', controller=controller,
                    action='render_contribute')
        return map

    """
    def after_map(self, map):
        return

    def is_fallback(self):
        return False

    # Note: Make sure that this is the correct package_type
    def package_types(self):
        return ['dataset']
    """