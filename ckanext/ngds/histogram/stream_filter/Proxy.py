

class Proxy():
    """
    This class represents a proxy that persists a WFS locally for faster streaming.
    It also offers extra features such as calculating statistics and creating graphs
    """

    def __init__(self, url, version="1.0.0"):
        self.wfs = WebFeatureService(url, version=version)
        self.type = self.wfs.identification.type
        self.version = self.wfs.identification.version
        self.title = self.wfs.identification.title
        self.abstract = self.wfs.identification.abstract

    def printCapabilities(self):
        print("no Capabilities");

    def printItems(self):
        print("no Items");


p = Proxy();

p.printCapabilities();
p.printItems();




