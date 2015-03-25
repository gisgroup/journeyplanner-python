from . import exceptions, config
from .requester import Requester

from xml.etree.ElementTree import ElementTree


class Client:
    def __init__(self, username, password):
        self.requester = Requester(config.API_ENDPOINT, username, password)

    def location(self, input=None):
        """Location service. Converts input into a list of geographic points.

        Returns:
          List of {lon:xy.z,lat:xy.z} dicts
        """
        elements = self._request('/locations', input=input)

        for element in elements:
            location = {
                'name': element.get('name'),
                'longitude':
                    int(element.get('x')) / config.COORDINATE_MULTIPLIER,
                'latitude':
                    int(element.get('y')) / config.COORDINATE_MULTIPLIER,
            }

            if element.tag == 'CoordLocation':
                if element.get('type') == 'ADR':
                    location['type'] = 'address'
                if element.get('type') == 'POI':
                    location['type'] = 'poi'
            if element.tag == 'StopLocation':
                location['id'] = int(element.get('id'))
                location['type'] = 'stop'

            yield location

    def stopsnearby(self, **input):
        """The stops nearby service will deliver all stops within a radius of a
        given coordinate. Each stop location contains the name of the
        station/stop, the coordinate, the id and the distance from the request
        coordinate in meters. All distances are as the crow flies and not
        routed.

        Args:
            coordX, coordY for the coordinate and
            maxRadius, maxNumber to limit the result list.
                The maximum radius is defined in meters. The maximum number
                limits the length of the returned list accordingly.

        Yields:
            dict: The next location in the result

        Examples:
            A request to ask for maximum 30 stops near a given coordinate and a
            radius of
            maximum 1000m looks like follows:

            >>> client.stopsnearby(coordX=12565796,
                                   coordY=5567306,
                                   maxRadius=1000,
                                   maxNumber=30)
            [0, 1, 2, 3]
        """
        elements = self._request('/stopsNearby', **input)

        for element in elements:
            location = {
                'id': int(element.get('id')),
                'name': element.get('name'),
                'longitude':
                    int(element.get('x')) / config.COORDINATE_MULTIPLIER,
                'latitude':
                    int(element.get('y')) / config.COORDINATE_MULTIPLIER,
                'distance_meters': int(element.get('distance'))
            }

            yield location

    def _request(self, path, **query):
        response = self.requester.get(path, **query)

        tree = ElementTree()
        tree.parse(response)
        root = tree.getroot()

        error = root.get('error')
        if error:
            raise exceptions.exception_from_message(error)
        else:
            return root
