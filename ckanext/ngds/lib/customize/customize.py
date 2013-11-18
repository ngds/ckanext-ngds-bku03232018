__author__ = 'kaffeine'
import ckan.model as model


class Customize(object):
    def customize(self):
        from pylons import config

        group_name = config.get('ngds.default_group_name', 'public')
        check = model.group.Group.by_name(group_name)
        print check
        if not check:
            # Then create
            model.repo.new_revision()
            new_group = model.group.Group(group_name)
            new_group.is_organization = True
            model.Session.add(new_group)
            model.repo.commit_and_remove()