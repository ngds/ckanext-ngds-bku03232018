import ckan.plugins as p
import ckan.model as model

class NGDSClient(p.SingletonPlugin):


    p.implements(p.IConfigurer, inherit=True)

    """
    p.implements(p.IActions)
    p.implements(p.IAuthFunctions)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IFacets)
    p.implements(p.ITemplateHelpers)
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

    """
    def before_map(self, map):
        controller = 'ckanext.ngds.controllers.view:ViewController'
        return

    def after_map(self, map):
        return

    def is_fallback(self):
        return False

    # Note: Make sure that this is the correct package_type
    def package_types(self):
        return ['dataset']
    """