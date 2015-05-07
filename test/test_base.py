from journeyplanner import JourneyPlanner, error
from journeyplanner.request import _parse

from io import StringIO

import unittest


class TestService(unittest.TestCase):

    def test_fail_authentication(self):
        jp = JourneyPlanner()
        jp.authenticate('foo', 'bar')
        with self.assertRaises(error.AuthenticationError):
            next(jp.location('elmegade 5 københavn'))

    def test_unauthenticated(self):
        jp = JourneyPlanner()
        first = next(jp.location('elmegade 5 københavn'))
        self.assertEqual(first.latitude, 55.68954)
        self.assertEqual(first.longitude, 12.558038)

if __name__ == '__main__':
    unittest.main()
