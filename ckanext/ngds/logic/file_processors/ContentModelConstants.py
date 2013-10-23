__author__ = 'kaffeine'


class ContentModelValue(object):
    def __init__(self, cm, cmv):
        self.cm = cm
        self.cmv = cmv

    def __hash__(self):
        det = self.cm + self.cmv
        for c in det:
            hash = 101 * hash + ord(c)

    def __eq__(self, other):
        return self.cm == other.cm and self.cmv == other.cmv


BHT_1_5 = ContentModelValue('http://schemas.usgin.org/uri-gin/ngds/dataschema/boreholetemperature/',
                            'http://schemas.usgin.org/uri-gin/ngds/dataschema/boreholetemperature/1.5')