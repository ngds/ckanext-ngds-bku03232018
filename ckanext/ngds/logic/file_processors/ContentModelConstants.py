__author__ = 'kaffeine'


class ContentModelValue(object):
    def __init__(self, cm, cmv):
        self.cm = cm
        self.cmv = cmv

    def __hash__(self):
        det = self.cm + self.cmv
        hash = 0
        for c in det:
            hash = 101 * hash + ord(c)
        return hash

    def __eq__(self, other):
        return self.cm == other.cm and self.cmv == other.cmv


BHT_1_5 = ContentModelValue('http://schemas.usgin.org/uri-gin/ngds/dataschema/boreholetemperature/',
                            'http://schemas.usgin.org/uri-gin/ngds/dataschema/boreholetemperature/1.5')