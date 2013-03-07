from pylons.i18n import _

import ckan.logic as logic
import ckan.new_authz as new_authz


def manage_users(context, data_dict):

    model = context['model']
    user = context.get('user','')
    print "User Logged: ",user
    if new_authz.is_sysadmin(user):
        return { 'success': True}
    return { 'success': False,'msg': _('User %s not authorized to manage users') % (str(user))}

"""
This method got to check whether user has access to publish dataset based on his role.
"""
def publish_dataset(context, data_dict):

	model = context['model']
	user = context.get('user','')
	print "User Logged: ",user
	check1 = new_authz.has_user_permission_for_group_or_org('public', user, 'publish_dataset')
	if not check1:
		return {'success': False, 'msg': _('User %s not authorized to publish dataset') % (str(user))}
	return {'success': True}    