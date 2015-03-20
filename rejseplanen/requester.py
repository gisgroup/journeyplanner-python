"""
.requester
~~~~~~~~~~~~~~~~~~~
Helper for performing authenticated http requests
"""

from urllib import request
from urllib.parse import urlencode

class Requester:
  def __init__(self, base_url, username, password):
    self.base_url = base_url
    passman = request.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, base_url, username, password)
    auth_handler = request.HTTPBasicAuthHandler(passman)
    self.opener = request.build_opener(auth_handler)

  def get(self, path, **query):
    tuples = sorted(query.items(), key = lambda x:x[0] )
    querystring = urlencode(tuples)
    url = '%s%s?%s' % (self.base_url, path, querystring)

    return self.opener.open(url)
