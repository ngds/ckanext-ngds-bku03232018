import ckan.plugins as p
from ckanext.ngds.common import model
import ckanext.ngds.sysadmin.model.db as db

class SystemAdministrator(p.SingletonPlugin):

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IConfigurable, inherit=True)
    p.implements(p.IRoutes, inherit=True)

    def configure(self, config):

        data = {
            'ngds_publish': config.get('ngds.publish'),
            'ngds_harvest': config.get('ngds.harvest'),
            'ngds_edit_metadata': config.get('ngds.edit_metadata'),
            'ckan_site_title': config.get('ckan.site_title'),
            'ckan_main_css': config.get('ckan.main_css'),
            'ckan_site_description': config.get('ckan.site_description'),
            'ckan_site_logo': config.get('ckan.site_logo'),
            'ckan_site_about': config.get('ckan.site_about'),
            'ckan_site_intro_text': config.get('ckan.site_intro_text'),
            'ckan_homepage_style': config.get('ckan.homepage_style'),
        }

        db.init_table_populate(model, data)

    def update_config(self, config):
        """
        Extends 'update_config' function in IConfigurer object.  Registers the
        templates and static files directories with CKAN.

        @config: Pylons global config object
        """
        data = db.init_config_show(model)
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