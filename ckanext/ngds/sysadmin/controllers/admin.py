import ckanext.ngds.sysadmin.model.db as db
from ckanext.ngds.common import base, admin, app_globals, config, h

request = base.request
_ = base._

# Register ngds admin configurations with pylons
app_globals.mappings['ngds.publish'] = 'ngds.publish'
app_globals.mappings['ngds.harvest'] = 'ngds.harvest'
app_globals.mappings['ngds.edit_metadata'] = 'ngds.edit_metadata'

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
            {'name': 'ngds.edit_metadata', 'control': 'select', 'options': data_controls, 'label': _('Metadata Editing'), 'placeholder': ''},
        ]
        return items

    def config(self, items):
        """
        Renders global config items based on user input in the UI.  Returns a
        dictionary of config parameters that are used to build the admin config
        Jinja templates.

        @param items: pylons global config options
        @return: dictionary
        """

        data = request.POST

        def update_config(items, data, config):
            if db.sysadmin_config_table is None:
                db.init()
            for item in items:
                name = item['name']
                if name in data:
                    app_globals.set_global(name, data[name])
            app_globals.reset()
            h.redirect_to(controller=self.controller, action=config)

        if 'save-data-config' in data:
            update_config(items, data, 'data_config')

        if 'save-style-config' in data:
            update_config(items, data, 'style_config')

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