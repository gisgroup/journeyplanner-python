from . import exceptions, config
from .requester import Requester

import logging
from datetime import datetime, timedelta
from xml.etree.ElementTree import ElementTree

class Client:
  def __init__(self, username, password):
    self.requester = Requester(config.API_ENDPOINT, username, password)

  def location(self, input):
    """Location service. Converts input into a list of geographic points.

    Returns:
      List of {lon:xy.z,lat:xy.z} dicts
    """
    locations = self._request('/locations', input=input)

    # map each location to lon/lat dict
    return [
      dict( longitude=int(location.attrib['x']) / config.COORDINATE_MULTIPLIER
          , latitude=int(location.attrib['y']) / config.COORDINATE_MULTIPLIER
          ) for location in locations
    ]

  #-------------------------------------------------------------------------------

  def _request(self, path, **query):
    response = self.requester.get('/location', **query)

    tree = ElementTree()
    tree.parse(response)
    root = tree.getroot()

    error = root.get('error')
    if error:
      raise exceptions.exception_from_message(error)
    else:
      return root
