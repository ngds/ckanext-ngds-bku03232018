import ckan.plugins as p
import ckanext.ngds.sysadmin.model.db as db

import ckan.lib.app_globals as app_globals
import ckan.model as model

import ckanext.ngds.sysadmin.helpers as h

class SystemAdministrator(p.SingletonPlugin):

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IPackageController, inherit=True)

    def update_config(self, config):
        """
        Use this function to hook into the pylons global config object before
        the server starts up.  The call to read configurations from the
        'ngds_system_info' table happens after they are read from the vanilla
        CKAN 'system_info' table, therefore ensuring that custom configurations
        get used over vanilla ones.

        @config: Pylons global config object
        """

        # Register ngds admin configurations with pylons
        app_globals.mappings['ngds.publish'] = 'ngds.publish'
        app_globals.mappings['ngds.harvest'] = 'ngds.harvest'
        app_globals.mappings['ngds.edit_metadata'] = 'ngds.edit_metadata'
        app_globals.mappings['ngds.featured_data'] = 'ngds.featured_data'

        # Collect config data to populate 'ngds_system_info' table if this is
        # the first time this server is booting up with the 'sysadmin' plugin.
        # Initially, this table will be populated with either what it finds in
        # the config file or default values.
        data = {
            'ngds.publish': config.get('ngds.publish', 'True'),
            'ngds.harvest': config.get('ngds.harvest', 'True'),
            'ngds.edit_metadata': config.get('ngds.edit_metadata', 'True'),
            'ngds.featured_data': config.get('ngds.featured_data', None)
        }

        # If this is the first time booting up the server with the 'sysadmin'
        # plugin, then build the 'ngds_system_info' table, populate it with the
        # default values and build ORM.  Otherwise, just build the ORM.
        db.init_table_populate(model, data)

        # Always read the 'ngds_system_info' table upon starting the server
        db_config = db.init_config_show(model)

        # Update pylons global config object with the configs we just read from
        # the 'ngds_system_info' table.
        config.update(db_config)

        # Add custom templates directory
        p.toolkit.add_template_directory(config, 'templates')

        # Add public assets directory
        p.toolkit.add_public_directory(config, 'public')

        # Register fanstatic directory for JavaScript files
        p.toolkit.add_resource('fanstatic', 'sysadmin')

    def before_map(self, map):
        # Set routes for controller
        controller = 'ckanext.ngds.sysadmin.controllers.admin:NGDSAdminController'
        map.connect('sysadmin_style_config', '/ckan-admin/style-config',
                    controller=controller, action='style_config',
                    ckan_icon='check')
        map.connect('sysadmin_operating_config', '/ckan-admin/operating-config',
                    controller=controller, action='operating_config',
                    ckan_icon='check')
        map.connect('sysadmin_data_config', '/ckan-admin/data-config',
                    controller=controller, action='data_config',
                    ckan_icon='check')

        controller = 'ckanext.ngds.sysadmin.controllers.view:ViewController'
        map.connect('ngds_homepage_search', '/ngds/search',
                    controller=controller, action='homepage_search')
        return map

    def get_helpers(self):
        return {'data_publish_enabled': h.data_publish_enabled,
                'data_harvest_enabled': h.data_harvest_enabled,
                'metadata_edit_enabled': h.metadata_edit_enabled,
                'get_featured_data': h.get_featured_data,
                'get_recent_activity': h.get_recent_activity,
                'get_formatted_date': h.get_formatted_date
                }

    def after_delete(self, context, data_dict):
        ''' Adds the "permanentently deleted message '''
        import ckan.lib.helpers as h

        package_dict = p.toolkit.get_action('package_show')(context, {'id': data_dict['id']})
        
        if 'type' in package_dict and package_dict['type'] == 'harvest':
            h.flash_success('Harvesting source will be permanently deleted in approximately 5 minutes')
