import ckanext.ngds.metadata.logic.action as action
from ckanext.ngds.common import plugins as p

class MetadataPlugin(p.SingletonPlugin):

    p.implements(p.IConfigurer)
    p.implements(p.IActions)
    p.implements(p.IRoutes, inherit=True)

    def update_config(self, config):
        templates = 'templates'
        p.toolkit._add_template_directory(config, templates)

    def before_map(self, map):
        controller = 'ckanext.ngds.metadata.controllers.view:ViewController'
        map.connect('metadata_iso_19139', '/metadata/iso_19139/:id',
                    controller=controller, action='show_iso_19139')
        return map

    def get_actions(self):
        return {
            'iso_19139': action.iso_19139,
        }