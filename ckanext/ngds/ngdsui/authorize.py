''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

from pylons.i18n import _

import ckan.new_authz as new_authz

from ckanext.ngds.ngdsui.misc import helpers


def manage_users(context, data_dict):
    model = context['model']
    user = context.get('user','')
    print "User Logged: ",user
    if new_authz.is_sysadmin(user):
        return { 'success': True}
    return { 'success': False,'msg': _('User %s not authorized to manage users') % (str(user))}

def publish_dataset(context, data_dict):
    """
    This method got to check whether user has access to publish dataset based on his role.
    """

    model = context['model']
    user = context.get('user','')
    print "User Logged: ",user
    #Change the group to be coming from global setting...
    check1 = new_authz.has_user_permission_for_group_or_org(helpers.get_default_group(), user, 'publish_dataset')
    if not check1:
        return {'success': False, 'msg': _('User %s not authorized to publish dataset') % (str(user))}
    return {'success': True}

def manage_nodes(context, data_dict):

    model = context['model']
    user = context.get('user','')
    print "User Logged: ",user
    if new_authz.is_sysadmin(user):
        return { 'success': True}
    return { 'success': False,'msg': _('User %s not authorized to manage nodes') % (str(user))}

def execute_bulkupload(context, data_dict):

    model = context['model']
    user = context.get('user','')
    print "User Logged: ",user
    if new_authz.is_sysadmin(user):
        return { 'success': True}
    return { 'success': False,'msg': _('User %s not authorized to execute the bulk upload process') % (str(user))}    
