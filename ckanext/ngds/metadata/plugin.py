import ckanext.ngds.metadata.logic.action as action
from ckanext.ngds.common import plugins as p

class MetadataPlugin(p.SingletonPlugin, p.toolkit.DefaultDatasetForm):

    p.implements(p.IConfigurer)
    p.implements(p.IActions)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IDatasetForm)

    # IConfigurer
    def update_config(self, config):
        templates = 'templates'
        public = 'public'
        p.toolkit.add_template_directory(config, templates)
        p.toolkit.add_public_directory(config, public)

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
        }

    # IDatasetForm
    def _modify_package_schema(self, schema):
        schema.update({
            'authors': [p.toolkit.get_validator('ignore_missing'),
                        p.toolkit.get_converter('convert_to_extras')],
            'dataset_category': [p.toolkit.get_validator('ignore_missing'),
                                 p.toolkit.get_converter('convert_to_extras')],
            'dataset_lang': [p.toolkit.get_validator('ignore_missing'),
                             p.toolkit.get_converter('convert_to_extras')],
            'dataset_uri': [p.toolkit.get_validator('ignore_missing'),
                            p.toolkit.get_converter('convert_to_extras')],
            'lineage': [p.toolkit.get_validator('ignore_missing'),
                        p.toolkit.get_converter('convert_to_extras')],
            'maintainers': [p.toolkit.get_validator('ignore_missing'),
                            p.toolkit.get_converter('convert_to_extras')],
            'other_id': [p.toolkit.get_validator('ignore_missing'),
                         p.toolkit.get_converter('convert_to_extras')],
            'publication_date': [p.toolkit.get_validator('ignore_missing'),
                                 p.toolkit.get_converter('convert_to_extras')],
            'quality': [p.toolkit.get_validator('ignore_missing'),
                        p.toolkit.get_converter('convert_to_extras')],
            'spatial': [p.toolkit.get_validator('ignore_missing'),
                        p.toolkit.get_converter('convert_to_extras')],
            'status': [p.toolkit.get_validator('ignore_missing'),
                       p.toolkit.get_converter('convert_to_extras')],
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
        schema.update({
            'authors': [p.toolkit.get_validator('ignore_missing'),
                        p.toolkit.get_converter('convert_from_extras')],
            'dataset_category': [p.toolkit.get_validator('ignore_missing'),
                                 p.toolkit.get_converter('convert_from_extras')],
            'dataset_lang': [p.toolkit.get_validator('ignore_missing'),
                             p.toolkit.get_converter('convert_from_extras')],
            'dataset_uri': [p.toolkit.get_validator('ignore_missing'),
                            p.toolkit.get_converter('convert_from_extras')],
            'lineage': [p.toolkit.get_validator('ignore_missing'),
                        p.toolkit.get_converter('convert_from_extras')],
            'maintainers': [p.toolkit.get_validator('ignore_missing'),
                            p.toolkit.get_converter('convert_from_extras')],
            'other_id': [p.toolkit.get_validator('ignore_missing'),
                         p.toolkit.get_converter('convert_from_extras')],
            'publication_date': [p.toolkit.get_validator('ignore_missing'),
                                 p.toolkit.get_converter('convert_from_extras')],
            'quality': [p.toolkit.get_validator('ignore_missing'),
                        p.toolkit.get_converter('convert_from_extras')],
            'spatial': [p.toolkit.get_validator('ignore_missing'),
                        p.toolkit.get_converter('convert_from_extras')],
            'status': [p.toolkit.get_validator('ignore_missing'),
                       p.toolkit.get_converter('convert_from_extras')],
        })
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # packages not handled by any other IDatasetForm plugin
        return True

    def package_types(self):

        return []