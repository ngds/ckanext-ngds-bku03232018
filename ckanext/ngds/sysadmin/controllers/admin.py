import datetime
import ckanext.ngds.sysadmin.model.db as db

from pylons import config
import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.lib.app_globals as app_globals
import ckan.model as model
import ckan.controllers.admin as admin

request = base.request
_ = base._

class NGDSAdminController(admin.AdminController):
    """
    Vanilla CKAN provides no working interface for extending it's admin
    functionality, so we have to inherit the AdminController object directly in
    order to extend object.  Then we redirect the routes in the plugin.py file
    to use this controller.
    """
    def __init__(self):
        self.controller = 'ckanext.ngds.sysadmin.controllers.admin:NGDSAdminController'

    def get_style_config_form_items(self):
        """
        Just a copy of the AdminController's _get_config_form_items function
        that we rename so that we can build and pass other config form item
        objects into the config method.

        @return: dictionary
        """
        styles = [{'text': 'Default', 'value': '/base/css/main.css'},
                  {'text': 'Red', 'value': '/base/css/red.css'},
                  {'text': 'Green', 'value': '/base/css/green.css'},
                  {'text': 'Maroon', 'value': '/base/css/maroon.css'},
                  {'text': 'Fuchsia', 'value': '/base/css/fuchsia.css'}]

        homepages = [{'value': '1', 'text': 'Introductory area, search, featured group and featured organization'},
                     {'value': '2', 'text': 'Search, stats, introductory area, featured organization and featured group'},
                     {'value': '3', 'text': 'Search, introductory area and stats'}]

        items = [
            {'name': 'ckan.site_title', 'control': 'input', 'label': _('Site Title'), 'placeholder': ''},
            {'name': 'ckan.main_css', 'control': 'select', 'options': styles, 'label': _('Style'), 'placeholder': ''},
            {'name': 'ckan.site_description', 'control': 'input', 'label': _('Site Tag Line'), 'placeholder': ''},
            {'name': 'ckan.site_logo', 'control': 'input', 'label': _('Site Tag Logo'), 'placeholder': ''},
            {'name': 'ckan.site_about', 'control': 'markdown', 'label': _('About'), 'placeholder': _('About page text')},
            {'name': 'ckan.site_intro_text', 'control': 'markdown', 'label': _('Intro Text'), 'placeholder': _('Text on home page')},
            {'name': 'ckan.homepage_style', 'control': 'select', 'options': homepages, 'label': _('Homepage'), 'placeholder': ''},
        ]
        return items

    def get_ngds_config_form_items(self):
        """
        Custom config form controls for NGDS data contribution and interaction.

        @return: dictionary
        """

        data_controls = [{'text': 'Enabled', 'value': 'True'},
                         {'text': 'Disabled', 'value': 'False'}]

        items = [{'name': 'ngds.publish', 'control': 'select', 'options': data_controls, 'label': _('Data Publishing'), 'placeholder': ''},
                 {'name': 'ngds.harvest', 'control': 'select', 'options': data_controls, 'label': _('Data Harvesting'), 'placeholder': ''},
                 {'name': 'ngds.edit_metadata', 'control': 'select', 'options': data_controls, 'label': _('Metadata Editing'), 'placeholder': ''}]

        return items

    def config(self, items):
        """
        If this method gets called from the vanilla admin page for custom UI
        settings, then we update the ckan.* config variables through the
        'app_globals' module and CKAN stores that information in the
        'system_info' table so that custom configs will persist through a server
        failure.  If this method gets called from the NGDS admin page for data
        settings, then the 'app_globals' module gets updated in memory but
        we write the configs to a custom 'ngds_system_info' table.

        @param items: pylons global config options
        @return: dictionary
        """
        data = request.POST

        if 'save-data-config' in data:
            # Set up ORM if it's not already set
            if db.ngds_system_info is None:
                db.init(model)
            # Get db data to update
            update_db = db.SysadminConfig.get(active_config=True)
            for item in items:
                name = item['name']
                if name in data:
                    # Update app_globals in memory
                    app_globals.set_global(name, data[name])
                    # Update database
                    setattr(update_db, name, data.get(name))
            app_globals.reset()
            update_db.last_edited = datetime.datetime.utcnow()
            update_db.save()
            session = model.Session
            session.add(update_db)
            session.commit()
            h.redirect_to(controller=self.controller,
                          action='data_config')

        if 'save-style-config' in data:
            for item in items:
                name = item['name']
                if name in data:
                    app_globals.set_global(name, data[name])
            app_globals.reset()
            h.redirect_to(controller=self.controller,
                          action='style_config')

        data = {}
        for item in items:
            name = item['name']
            data[name] = config.get(name)

        return {'data': data, 'errors': {}, 'form_items': items}

    def style_config(self):
        """
        Render the admin config page for style and page layout.

        @return: web page
        """
        items = self.get_style_config_form_items()
        vars = self.config(items)
        return base.render('admin/style-config.html',
                           extra_vars=vars)

    def data_config(self):
        """
        Render the admin config page for NGDS data contribution and interaction.

        @return: web page
        """
        items = self.get_ngds_config_form_items()
        vars = self.config(items)
        return base.render('admin/data-config.html',
                           extra_vars=vars)