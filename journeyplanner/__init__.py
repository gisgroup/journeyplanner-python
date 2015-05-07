from .request import Requester
from .resources import lat2y, lon2x, Location, Stop, Trip
from .config import COORDINATE_MULTIPLIER


class JourneyPlanner:
    def __init__(self):
        self.requester = Requester()

    def authenticate(self, username, password):
        self.requester.authenticate(username, password)

    def _stationboard(self, service):
        """The station board board can be retrieved by the service
        departureBoard. This method will return the next 20 departures (or less
        if not existing) from a given point in time.

        In addition to departure boards the service arrivalBoard delivers
        arriving journeys at a specified stop. The parameters are identical to
        the parameters of the departureBoard service.
        """
        tree = self.requester.get(service)
        pass

    def arrivalboard(self):
        return self._stationboard('arrivalBoard')

    def departureboard(self):
        return self._stationboard('departureBoard')

    def journeydetail(self):
        """The journeyDetail service will deliver information about the complete
        route of a vehicle. This service can’t be called directly but only by
        reference URLs in a result of a trip or departureBoard request. It
        contains a list of all stops/stations of this journey including all
        departure and arrival times (with realtime data if available) and
        additional information like specific attributes about facilities and
        other texts.
        """
        tree = self.requester.get('journeyDetail')
        pass

    def location(self, query):
        """The location service can be used to perform a pattern matching of a
        user input and to retrieve a list of possible matches in the journey
        planner database. Possible matches might be stops/stations, points of
        interest and addresses.
        """
        tree = self.requester.get('locations', input=query)

        yield from (Location(element) for element in tree)

    def multidepartureboard(self):
        """The multi departure board is a combined departure board for up to 10
        different stops. It can be retrieved by a service called
        multiDepartureBoard. This method will return the next 20 departures (or
        less if not existing) of the defined stops from a given point in time.
        """
        tree = self.requester.get('multiDepartureBoard')
        pass

    def stopsnearby(self, *, latitude, longitude, radius=None, limit=None):
        """The stops nearby service will deliver all stops within a radius of a
        given coordinate.

        Each stop location contains the name of the
        station/stop, the coordinate, the id and the distance from the request
        coordinate in meters. All distances are as the crow flies and not
        routed.
        """
        tree = self.requester.get('stopsNearby',
                                  coordX=lon2x(longitude),
                                  coordY=lat2y(latitude),
                                  maxRadius=radius,
                                  maxNumber=limit)

        yield from (Stop(element) for element in tree)

    def trip(self, *, origin, destination,
             date=None, time=None,
             via=None, arrival=False,
             bus=True, metro=True, train=True):
        """The trip service calculates a trip from a specified origin to a
        specified destination. These might be stop/station IDs or coordinates
        based on addresses and points of interest validated by the location
        service or coordinates freely defined by the client.

        The parameters are named either originId or originCoordX, originCoordY,
        and originCoordName. For the destination the parameters are named either
        destId or destCoordX, destCoordY and destCoordName
        """
        tree = self.requester.get('trip',
                                  originId=origin,
                                  destId=destination,
                                  #date=date,
                                  #time=time,
                                  #viaId=via,
                                  searchForArrival=1 if arrival else 0,
                                  useBus=1 if bus else 0,
                                  useMetro=1 if metro else 0,
                                  useTrain=1 if train else 0)

        yield from (Trip(element) for element in tree)
