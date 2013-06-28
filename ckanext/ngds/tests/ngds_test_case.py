from unittest import TestCase
from postgis_sql import POSTGIS, SPATIAL_REF_SYS
from ckanext.ngds.env import ckan_model as model
from ckan.plugins import toolkit

class NgdsTestCase(TestCase):
    _sys_admin = None
    _public_org = None

    @classmethod
    def setUpClass(cls):
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
            print "TABLE GENERATION FAILED: %s" % ex.orig

        session.close()

        # Build plugin tables
        from ckanext.harvest.model import setup as harvest_tables
        harvest_tables()

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
            org = dict(
                name="public",
                users=[{"name": self.admin_user().name}]
            )
            self._public_org = toolkit.get_action("organization_create")({"user": self.admin_user().name}, org)
        return self._public_org

    def add_package(self, package_name, package_dict={}):
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
        return toolkit.get_action("package_create")({"user": self.admin_user().name}, package)

    def add_resource(self, resource_dict):
        pass

    def ngds_table_set_up(self):
        pass