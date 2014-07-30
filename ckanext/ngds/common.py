# Truth is, we can't get everything we need out of ckan.plugins.toolkit because
# not everything we need to extend is exposed through that interface.  This
# file exists as a central place to organize these kinds of dependencies, so
# that we can easily update our code in the future as changes are made in the
# trunk branch of CKAN

from pylons import config
import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.lib.app_globals as app_globals
import ckan.model as model
import ckan.logic as logic
import ckan.controllers.admin as admin
import ckan.tests as tests
import ckan.plugins as plugins
import ckan.config.middleware as middleware