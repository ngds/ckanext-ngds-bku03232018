__author__ = 'adrian'

import logging

import ckan.plugins as p
from ckan.plugins import ITemplateHelpers, IRoutes, IResourcePreview
import ckanext.ngds.contentmodel.logic.action as action
import ckan.logic as logic

log = logging.getLogger(__name__)
_get_or_bust = logic.get_or_bust

class USGINContentModelPlugin(p.SingletonPlugin):
    '''
    Geoserver plugin.

    This plugin provides actions to "spatialize" tables in the datastore and to connect them with the Geoserver. Spatialize
    means:
    1. Create an additional column of type (PostGIS) point
    2. Update the column with values calulated from already existing latitude/ longitude columns

    Connect to Geoserver means:
    1. Create a select statement
    2. Use the geoserver API to create a new layer using that select statement

    '''
    # p.implements(p.IConfigurable, inherit=True)
    p.implements(p.IActions)
    p.implements(p.IAuthFunctions)

    def get_actions(self):

        actions = {
            'geoserver_publish_usgin_layer': action.publish_usgin_layer
        }

        return actions
