from ckan.plugins.interfaces import Interface

class IAdminController(Interface):
    """
    Hook into the admin controller, mostly just to extend the custom config
    options that the admin can set in the UI.  Vanilla CKAN currently only
    supports extending the admin interface through Jinja2 macros which all fail.
    """

    def get_config_form_items(self):
        """
        Set configuration items in the CKAN administrator UI, which will be used
        as method parameters in the 'form.autoform()' Jinja2 macro.

        Example:

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
            {'name': 'ckan.site_custom_css', 'control': 'textarea', 'label': _('Custom CSS'), 'placeholder': _('Customisable css inserted into the page header')},
            {'name': 'ckan.homepage_style', 'control': 'select', 'options': homepages, 'label': _('Homepage'), 'placeholder': ''},
        ]
        return items

        @return: [{items}]
        """
        pass

    def reset_config(self):
        """
        Reset global pylons configuration object to the defaults set in the
        development.ini file.

        @return: render 'admin/confirm_reset.html'
        """
        pass

    def config(self):
        """
        Builds the admin configuration UI with the correct parameters in the
        pylons global configuration object.  Updates the pylons global
        configuration object with changed parameters if the user selects to
        do so in the UI.

        @return: render 'admin/config.html'
        """
        pass

    def index(self):
        """
        Generate a list of all admins in the system.

        @return: render 'admin/index.html'
        """
        pass

    def trash(self):
        """
        Not really sure what this does yet.

        @return: Null?
        """
        pass
