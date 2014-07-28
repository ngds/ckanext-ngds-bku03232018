import ckan.plugins as p

class SystemAdministrator(p.SingletonPlugin):

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IRoutes, inherit=True)

    def update_config(self, config):
        """
        Extends 'update_config' function in IConfigurer object.  Registers the
        templates and static files directories with CKAN.

        @config: Pylons global config object
        """
        p.toolkit.add_template_directory(config, 'templates')

    def before_map(self, map):
        controller = 'ckanext.ngds.sysadmin.controllers.admin:NGDSAdminController'
        map.connect('ckanadmin_style_config', '/ckan-admin/style-config',
                    controller=controller, action='style_config',
                    ckan_icon='check')
        map.connect('ckanadmin_data_config', '/ckan-admin/data-config',
                    controller=controller, action='data_config',
                    ckan_icon='check')
        return map