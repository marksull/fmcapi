"""
Test api_objects.py
"""
import unittest

from fmcapi import api_objects


class TestApiObjects(unittest.TestCase):

    def test_ip_host_required_for_put(self):
        self.assertEqual(api_objects.IPHost.REQUIRED_FOR_PUT, ['id', 'name', 'value'])

