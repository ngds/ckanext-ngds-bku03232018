"""
Sometimes we need access to CKAN objects that we can't get at through
    ckan.plugins.toolkit. If we import those things here and need to adjust
    in the future, we can do that adjustment in one place.

This also allows us to "spoof" CKAN objects we need, without relying directly on CKAN, e.g. Session
"""

# If you have to use ckan.model...
from ckan import model as ckan_model


# Create a CKAN database session without relying on CKAN
def _setup():
    """Define a SQLAlchemy Session from ckan_config"""
    from pylons import config as ckan_config
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    db_str = ckan_config.get("sqlalchemy.url")
    return sessionmaker(bind=create_engine(db_str, echo=False))

Session = _setup()
