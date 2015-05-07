from . import config

def lat2y(latitude):
    return int(latitude * COORDINATE_MULTIPLIER)

def lon2x(longitude):
    return int(longitude * COORDINATE_MULTIPLIER)

def y2lat(y):
    return y / config.COORDINATE_MULTIPLIER

def x2lon(x):
    return x / config.COORDINATE_MULTIPLIER

class Resource:
    def __repr__(self):
        return repr(self.__dict__)

class Location(Resource):
    def __init__(self, element):
        self.name = element.get('name')
        self.longitude = x2lon(int(element.get('x')))
        self.latitude = y2lat(int(element.get('y')))

        if element.tag == 'StopLocation':
            self.type = 'stop'
            self.id = int(element.get('id'))

        if element.tag == 'CoordLocation':
            self.id = None
            if element.get('type') == 'ADR':
                self.type = 'address'
            if element.get('type') == 'POI':
                self.type = 'poi'


class Stop(Resource):
    def __init__(self, element):
        self.id = int(element.get('id'))
        self.name = element.get('name')
        self.latitude = int(element.get('y')) / config.COORDINATE_MULTIPLIER
        self.longitude = int(element.get('x')) / config.COORDINATE_MULTIPLIER

        try:
            self.distance = int(element.get('distance'))
        except ValueError:
            self.distance = None


class Leg(Resource):
    def __init__(self, leg):
        self.name = leg.get('name')
        self.type = leg.get('type')
        self.origin = leg.find('Origin').attrib
        self.destination = leg.find('Destination').attrib

        try:
            self.notes = leg.find('Notes').get('text')
        except AttributeError:
            self.notes = None

        try:
            self.ref = leg.find('JourneyDetailRef').get('ref')
        except AttributeError:
            self.ref = None

class Trip(Resource):
    def __init__(self, legs):
        self.legs = [Leg(leg) for leg in legs]
