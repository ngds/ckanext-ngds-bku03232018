from ckanext.ngds.common import base, admin, app_globals, config, h

request = base.request
_ = base._

app_globals.mappings['ngds.deployment'] = 'ngds.deployment'

class NGDSAdminController(admin.AdminController):

    def get_config_form_items(self):
        deployment_types = [{'text': 'NGDS Aggregator', 'value': 'ngds_aggregator'},
                            {'text': 'NGDS Publisher', 'value': 'ngds_publisher'}]

        styles = [{'text': 'Default', 'value': '/base/css/main.css'},
                  {'text': 'Red', 'value': '/base/css/red.css'},
                  {'text': 'Green', 'value': '/base/css/green.css'},
                  {'text': 'Maroon', 'value': '/base/css/maroon.css'},
                  {'text': 'Fuchsia', 'value': '/base/css/fuchsia.css'}]

        homepages = [{'value': '1', 'text': 'Introductory area, search, featured group and featured organization'},
                     {'value': '2', 'text': 'Search, stats, introductory area, featured organization and featured group'},
                     {'value': '3', 'text': 'Search, introductory area and stats'}]

        items = [
            {'name': 'ngds.deployment', 'control': 'select', 'options': deployment_types, 'label': _('Deployment'), 'placeholder': ''},
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

    def config(self):

        items = self.get_config_form_items()
        data = request.POST
        if 'save' in data:
            # update config from form
            for item in items:
                name = item['name']
                if name in data:
                    app_globals.set_global(name, data[name])
            app_globals.reset()
            h.redirect_to(controller='admin', action='config')

        data = {}
        for item in items:
            name = item['name']
            data[name] = config.get(name)

        vars = {'data': data, 'errors': {}, 'form_items': items}
        return base.render('admin/config.html',
                           extra_vars = vars)