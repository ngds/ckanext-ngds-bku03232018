from unittest import TestCase
from postgis_sql import POSTGIS, SPATIAL_REF_SYS

class NgdsTestCase(TestCase):
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

    def ngds_table_set_up(self):
        pass