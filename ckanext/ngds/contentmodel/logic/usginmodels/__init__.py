"""
Here we get to define a public API people can use when they `import usginmodels`
"""
import re

from exceptions import *
from exceptions import InvalidUri, InvalidLayer
from model_cache import ModelCache

cache = ModelCache()
cache.refresh()

def refresh():
    """Check http://schemas.usgin.org/contentmodels.json for the most up-to-date description of available content models"""
    cache.refresh()

def get_models():
    """Return a List of ContentModel objects"""
    return cache.models

def get_uris(uri):
    """Given a URI return the uri of the Model and the uri of the Version, if known"""

    # Spilt apart the URI the find the last component
    uri_components = uri.split('/')
    last = uri_components[len(uri_components)-1]

    # If the URI ended with a slash remove the empty component that was created by the split
    if last == "":
        uri_components.pop()
        last = uri_components[len(uri_components)-1]

    # If the last component is a version number remove it and set the value of version_uri
    version_uri = ""
    if re.match("\d", last):
        uri_components.pop()
        version_uri = uri

    # Find Models that match the URI given
    model_uri = "/".join(uri_components) + "/"

    return model_uri, version_uri

def get_model(uri):
    """Given a URI return the Model object"""

    # Find the Models in the cache whose uri matches the given model uri
    model_uri, version_uri = get_uris(uri)
    model_matches = [m for m in cache.models if m.uri == model_uri]

    # If there are no matches, raise an exception
    if len(model_matches) == 0:
        raise InvalidUri(uri)

    # If there is more than one model, we'll just take the first one
    return model_matches[0]

def get_version(uri):
    """Given a URI return the Version object"""

    # Find the Model for the uri
    model_uri, version_uri = get_uris(uri)
    model = get_model(model_uri)

    # Find the Version in the Model whose uri matches the given version uri
    if version_uri == "":
        version = model.latest_version()
    else:
        version_matches = [v for v in model.versions if v.uri == version_uri]

        # If there are no matches, raise an exception
        if len(version_matches) == 0:
            raise InvalidUri(version_uri)

        version = version_matches[0]

    return version

def get_layer(uri, layer_name = ""):
    """Given a URI and the layer name (optional) return the Layer object"""

    # Get the version for the uri
    version = get_version(uri)

    # Find the Layer in the Version that match the given layer name
    if layer_name == "":
        # If the layer name has not been specified and there is only one layer get the first layer
        # But if there is more than one layer, raise an exception
        if len(version.layers) == 1:
            layer = version.layers[0]
        else:
            raise Exception("Multilayer Model: Specify a layer.")
    else:
        layer_matches = [l for l in version.layers if l.layer_name == layer_name]

        # If there are no matches, raise an exception
        if len(layer_matches) == 0:
            raise InvalidLayer(layer_name)

        # If there is more than one layer, we'll just take the first one
        layer = layer_matches[0]

    return layer

def validate_file(csv_file, uri, layer_name = ""):
    """Return boolean and validation errors"""
    layer = get_layer(uri, layer_name)
    return layer.validate_file(csv_file)