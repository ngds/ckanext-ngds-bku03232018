from ckanext.ngds.common import plugins as p

class MapSearch(p.SingletonPlugin):

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IRoutes, inherit=True)

    """
    p.implements(p.ITemplateHelpers, inherit=True)
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

    def before_map(self, map):
        controller = 'ckanext.ngds.mapsearch.controllers.view:ViewController'
        map.connect('map_search', '/map_search', controller=controller,
                    action='render_map_search')
        return map