from unittest import TestCase
from postgis_sql import POSTGIS, SPATIAL_REF_SYS
from ckanext.ngds.env import ckan_model as model
from ckanext.ngds.env import ckan_logic
from ckan.plugins import toolkit
from ckanclient import CkanClient
import json

class NgdsTestCase(TestCase):
    _sys_admin = None
    _public_org = None
    _client = None

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

    '''
    Doesn't work -- CKAN isn't actually running during tests
    def client(self):
        if not self._client:
            self._client = CkanClient(base_location="http://localhost:5000/api", api_key=self.admin_user().apikey)
        return self._client
    '''

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
            maintainer="someone",
            maintainer_email="default@someone.com",
            owner_org=self.public_org()["name"],
            private=False,
            state="active",
            resources=[]
        )

        package.update(package_dict)

        if ngds_extras:
            package["extras"] = package.get("extras", [])
            default_extras = [
                {"key": "data_type", "value": "Dataset"},
                {"key": "publication_date", "value": "2013-07-01T00:00:00"},
                {"key": "location", "value": json.dumps(["San Diego, CA"])},
                {"key": "other_id", "value": json.dumps([])}
            ]
            for extra in default_extras:
                if extra["key"] not in [e["key"] for e in package["extras"]]:
                    package["extras"].append(extra)

        return toolkit.get_action("package_create")({"user": self.admin_user().name}, package)

    def add_tags(self, package_id, tags=[]):
        context = {"user": self.admin_user().name}
        p = toolkit.get_action("package_show")(context, {"id": package_id})

        tag_dicts = [{"name": tag} for tag in tags]
        p.update({"tags": tag_dicts})

        return toolkit.get_action("package_update")(context, p)

    def vocabulary(self, name):
        """Retrieve or create a vocabulary"""
        context = {"user": self.admin_user().name}
        try:
            return toolkit.get_action("vocabulary_show")(context, {"id": name})
        except:
            return toolkit.get_action("vocabulary_create")(context, {"name": name, "tags": []})

    def add_facets(self, package_id, facets):
        """Add facets (vocab tags) to a package"""
        context = {"user": self.admin_user().name}

        p = toolkit.get_action("package_show")(context, {"id": package_id})
        tags = p.get("tags", [])

        for facet in facets:
            vocab = self.vocabulary(facet[0])
            tags.append({"name": facet[1], "vocabulary_id": vocab.get("id", "")})

        p["tags"] = tags
        return toolkit.get_action("package_update")(context, p)

    def add_resource(self, package_id, resource_dict):
        context = {"user": self.admin_user().name}
        p = toolkit.get_action("package_show")(context, {"id": package_id})
        resources = p.get("resources", [])
        res = toolkit.get_action("resource_create")(context, resource_dict)
        resources.append(res)
        p["resources"] = resources
        return toolkit.get_action("package_update")(context, p)

    def add_resources(self, package_id, resources):
        [self.add_resource(package_id, res) for res in resources]
        return toolkit.get_action("package_show")({"user": self.admin_user().name}, {"id": package_id})

    def ngds_table_set_up(self):
        pass