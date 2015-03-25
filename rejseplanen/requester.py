"""
.requester
~~~~~~~~~~~~~~~~~~~
Helper for performing authenticated http requests
"""

from urllib import request
from urllib.parse import urlencode


class Requester:
    def __init__(self, base, username, password):
        self.base = base
        manager = request.HTTPPasswordMgrWithDefaultRealm()
        manager.add_password(None, self.base, username, password)
        handler = request.HTTPBasicAuthHandler(manager)
        self.opener = request.build_opener(handler)

    def get(self, path, **query):
        tuples = sorted(query.items(), key=lambda x: x[0])
        querystring = urlencode(tuples)
        url = '%s%s?%s' % (self.base, path, querystring)

        return self.opener.open(url)
