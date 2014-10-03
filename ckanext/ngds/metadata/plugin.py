import json
import ckanext.ngds.metadata.logic.action as action
import ckanext.ngds.metadata.logic.converters as converters
import ckanext.ngds.metadata.logic.validators as validators
import ckanext.ngds.metadata.helpers as h
from ckanext.ngds.common import plugins as p
from ckanext.ngds.common import app_globals

class MetadataPlugin(p.SingletonPlugin, p.toolkit.DefaultDatasetForm):

    p.implements(p.IConfigurer)
    p.implements(p.IActions)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IDatasetForm)
    p.implements(p.ITemplateHelpers)

    # IConfigurer
    def update_config(self, config):
        templates = 'templates'
        public = 'public'

        p.toolkit.add_template_directory(config, templates)
        p.toolkit.add_public_directory(config, public)
        p.toolkit.add_resource('fanstatic', 'metadata')

        content_models = action.http_get_content_models()
        app_globals.mappings['ngds.content_models'] = 'ngds.content_models'
        data = {
            'ngds.content_models': config.get('ngds.content_models', content_models)
        }
        config.update(data)

    # IRoutes
    def before_map(self, map):
        controller = 'ckanext.ngds.metadata.controllers.view:ViewController'
        map.connect('metadata_iso_19139', '/metadata/iso-19139/{id}.xml',
                    controller=controller, action='show_iso_19139')
        return map

    # IActions
    def get_actions(self):
        return {
            'iso_19139': action.iso_19139,
            'get_content_models': action.get_content_models,
            'get_content_models_short': action.get_content_models_short,
            'usgin_validate': action.usgin_validate
        }

    # IDatasetForm
    def _modify_package_schema(self, schema):
        schema.update({
            'ngds_package': [p.toolkit.get_validator('ignore_missing'),
                             converters.convert_to_ngds_package_extras]
        })

        schema['resources'].update({
            'ngds_resource': [p.toolkit.get_validator('ignore_missing'),
                              converters.convert_to_ngds_package_extras],
            'url': [validators.is_usgin_valid_data]
        })

        return schema

    def create_package_schema(self):
        schema = super(MetadataPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(MetadataPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(MetadataPlugin, self).show_package_schema()
        schema['tags']['__extras'].append(p.toolkit.get_converter('free_tags_only'))
        schema.update({
            'ngds_package': [p.toolkit.get_validator('ignore_missing'),
                             p.toolkit.get_converter('convert_from_extras')]
        })

        schema['resources'].update({
            'ngds_resource': [p.toolkit.get_validator('ignore_missing'),
                              p.toolkit.get_converter('convert_from_extras')],
        })

        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # packages not handled by any other IDatasetForm plugin
        return True

    def package_types(self):
        return []

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'protocol_codes': h.protocol_codes,
            'ngds_package_extras_processor': h.ngds_package_extras_processor,
            'ngds_resource_extras_processer': h.ngds_resource_extras_processer,
            'ngds_check_package_for_content_model': h.ngds_check_package_for_content_model
        }