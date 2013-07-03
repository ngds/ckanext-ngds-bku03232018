from unittest import TestCase
from postgis_sql import POSTGIS, SPATIAL_REF_SYS
from ckanext.ngds.env import ckan_model as model
from ckanext.ngds.env import ckan_logic
from ckan.plugins import toolkit

class NgdsTestCase(TestCase):
    _sys_admin = None
    _public_org = None

    class ObjectSpoofer():
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    @classmethod
    def setUpClass(cls):
        # Do stuff you want to happen once for each TestCase class
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import create_engine
        from sqlalchemy.exc import ProgrammingError
        from pylons import config

        # Connect to the database
        Session = sessionmaker(bind=create_engine(config.get("sqlalchemy.url")))
        session = Session()

        # Create PostGIS tables
        try:
            session.execute(POSTGIS)
            session.commit()
            session.execute(SPATIAL_REF_SYS)
            session.commit()
        except ProgrammingError as ex:
            print "POSTGIS TABLE GENERATION FAILED: %s" % ex.orig

        session.close()

        # Build plugin tables
        from ckanext.harvest.model import setup as harvest_tables
        try:
            harvest_tables()
        except Exception as ex:
            print "HARVEST TABLE GENERATION FAILED: %s" % ex.message

    def admin_user(self):
        """Find/Create an admin user"""
        if not self._sys_admin:
            sys_admin = model.User.get('test_sysadmin')
            if not sys_admin:
                sys_admin = model.User(name='test_sysadmin', sysadmin=True)
                model.Session.add(sys_admin)
                model.Session.commit()
                model.Session.remove()
            self._sys_admin = sys_admin
        return self._sys_admin

    def public_org(self):
        if not self._public_org:
            try:
                public_org = toolkit.get_action("organization_show")(None, {"id": "public"})
            except ckan_logic.NotFound:
                org = dict(
                    name="public",
                    users=[{"name": self.admin_user().name}]
                )
                public_org = toolkit.get_action("organization_create")({"user": self.admin_user().name}, org)
            self._public_org = public_org
        return self._public_org

    def add_package(self, package_name, package_dict={}, ngds_extras=True):
        package = dict(
            name=package_name,
            title="Test title",
            notes="Test notes",
            owner_org=self.public_org()["name"],
            private=False,
            state="active",
            resources=[]
        )

        package.update(package_dict)

        if ngds_extras:
            package["extras"] = package.get("extras", [])
            package["extras"].extend([
                {"key": "publication_date", "value": "2013-07-01T00:00:00"},
                {"key": "location", "value": "San Diego, CA"}
            ])
        
        return toolkit.get_action("package_create")({"user": self.admin_user().name}, package)

    def add_tags(self, package_id, tags=[]):
        context = {"user": self.admin_user().name}
        p = toolkit.get_action("package_show")(context, {"id": package_id})

        tag_dicts = [{"name": tag} for tag in tags]
        p.update({"tags": tag_dicts})

        return toolkit.get_action("package_update")(context, p)

    def add_resource(self, resource_dict):
        pass

    def ngds_table_set_up(self):
        pass