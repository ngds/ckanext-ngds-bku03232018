import ckan.plugins as p
import ckanext.ngds.sysadmin.interfaces as ngds_interfaces

# Register IAdminController with CKAN plugins module
p.IAdminController = ngds_interfaces.IAdminController


class SystemAdministrator(p.SingletonPlugin):

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IAdminController, inherit=True)

    def update_config(self, config):
        """
        Extends 'update_config' function in IConfigurer object.  Registers the
        templates and static files directories with CKAN.

        @config: Pylons global config object
        """
        p.toolkit.add_template_directory(config, 'templates')

    def before_map(self, map):
        controller = 'ckanext.ngds.sysadmin.controllers.admin:NGDSAdminController'
        map.connect('ckanadmin_config', '/ckan-admin/config', controller=controller,
                    action='config', ckan_icon='check')
        return map