from ckan.lib.base import *
from ckan.lib.navl.dictization_functions import DataError, unflatten, validate
from ckan.lib.base import (request,
                           render,
                           BaseController,
                           model,
                           abort, h, g, c)
from ckan.model.resource import Resource
import ckanext.ngds.geoserver.logic.action as action
from pylons import config
from pylons.decorators import jsonify
from ckan.logic import (tuplize_dict,clean_dict,
                        parse_params,flatten_to_string_key,get_action,check_access,NotAuthorized)
from ckan.controllers.storage import StorageController,StorageAPIController
import ckan.controllers.storage as storage
import ckanext.ngds.contentmodel