"""
Test api_objects.py
"""
import mock
import unittest

from fmcapi import api_objects


class TestApiObjects(unittest.TestCase):

    def test_ip_host_required_for_put(self):
        self.assertEqual(api_objects.IPHost.REQUIRED_FOR_PUT, ['id', 'name', 'value'])

    @mock.patch('fmcapi.api_objects.APIClassTemplate.parse_kwargs')
    @mock.patch('fmcapi.api_objects.APIClassTemplate.valid_for_delete')
    def test_api_class_template_delete_on_bad_response(self, mock_valid, *_):
        """
        If send_to_api returns a None (because the API call failed) then do not process the response and just return the None
        """
        mock_valid.return_value = True
        mock_fmc = mock.Mock()
        mock_fmc.send_to_api.return_value = None
        api = api_objects.APIClassTemplate(fmc=mock_fmc)
        api.id = 'id'
        self.assertIsNone(api.delete())

