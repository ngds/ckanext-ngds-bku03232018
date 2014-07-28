import ckan.plugins as p

class NGDSSystemAdmin(p.SingletonPlugin):

    p.implements(p.IConfigurer, inherit=True)
    #p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.IRoutes, inherit=True)

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