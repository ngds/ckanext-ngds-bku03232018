
class InvalidUri(Exception):
    def __init__(self, uri):
        self.message = "The URI %s is invalid." % uri

    def __str__(self):
        return self.message

class InvalidLayer(Exception):
    def __init__(self, layer_name):
        self.message = "The layer name %s is invalid." % layer_name

    def __str__(self):
        return self.message