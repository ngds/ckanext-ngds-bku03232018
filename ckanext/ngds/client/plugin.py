from ckanext.ngds.common import plugins as p

class NGDSClient(p.SingletonPlugin):

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

    #def get_helpers(self):
    #    return {}

    def before_map(self, map):
        controller = 'ckanext.ngds.client.controllers.view:ViewController'
        map.connect('ngds_developers', '/ngds/developers', controller=controller,
                    action='render_developers')
        map.connect('ngds_help', '/ngds/help', controller=controller,
                    action='render_help')
        map.connect('ngds_contact', '/ngds/contact', controller=controller,
                    action='render_contact')
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