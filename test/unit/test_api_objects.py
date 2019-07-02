"""
Test api_objects.py
"""
import mock
import unittest

from fmcapi import api_objects
from fmcapi.fmc import FMC


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

    @mock.patch('fmcapi.api_objects.ACPRule.parse_kwargs')
    @mock.patch('fmcapi.fmc.FMC')
    def test_PREFIX_URL_1(self, mock_fmc, *_):
        """
        Test PREFIX_URL property
            - No URL params
        """
        a = api_objects.ACPRule(fmc=mock_fmc, acp_name='something')

        self.assertEqual('/policy/accesspolicies', a.PREFIX_URL)

    @mock.patch('fmcapi.api_objects.ACPRule.parse_kwargs')
    @mock.patch('fmcapi.fmc.FMC')
    def test_PREFIX_URL_2(self, mock_fmc, *_):
        """
        Test PREFIX_URL property
            - Category param
        """
        a = api_objects.ACPRule(fmc=mock_fmc, acp_name='something')
        a.category = 'something'

        self.assertEqual('/policy/accesspolicies?category=something', a.PREFIX_URL)

    @mock.patch('fmcapi.api_objects.ACPRule.parse_kwargs')
    @mock.patch('fmcapi.fmc.FMC')
    def test_PREFIX_URL_3(self, mock_fmc, *_):
        """
        Test PREFIX_URL property
            - insertBefore param
        """
        a = api_objects.ACPRule(fmc=mock_fmc, acp_name='something')
        a.insertBefore = 'something'

        self.assertEqual('/policy/accesspolicies?insertBefore=something', a.PREFIX_URL)

    @mock.patch('fmcapi.api_objects.ACPRule.parse_kwargs')
    @mock.patch('fmcapi.fmc.FMC')
    def test_PREFIX_URL_4(self, mock_fmc, *_):
        """
        Test PREFIX_URL property
            - insertAfter param
        """
        a = api_objects.ACPRule(fmc=mock_fmc, acp_name='something')
        a.insertAfter = 'something'

        self.assertEqual('/policy/accesspolicies?insertAfter=something', a.PREFIX_URL)

    @mock.patch('fmcapi.api_objects.ACPRule.parse_kwargs')
    @mock.patch('fmcapi.fmc.FMC')
    def test_PREFIX_URL_5(self, mock_fmc, *_):
        """
        Test PREFIX_URL property
            - category param
            - insertBefore param
        """
        a = api_objects.ACPRule(fmc=mock_fmc, acp_name='something')
        a.category = 'something'
        a.insertBefore = 'something'

        self.assertEqual('/policy/accesspolicies?category=something&insertBefore=something', a.PREFIX_URL)

    @mock.patch('fmcapi.api_objects.ACPRule.parse_kwargs')
    @mock.patch('fmcapi.fmc.FMC')
    def test_PREFIX_URL_6(self, mock_fmc, *_):
        """
        Test PREFIX_URL property
            - Category param
            - insertAfter param
        """
        a = api_objects.ACPRule(fmc=mock_fmc, acp_name='something')
        a.category = 'something'
        a.insertAfter = 'something'

        self.assertEqual('/policy/accesspolicies?category=something&insertAfter=something', a.PREFIX_URL)

    @mock.patch('fmcapi.api_objects.ACPRule.parse_kwargs')
    @mock.patch('logging.warning')
    @mock.patch('fmcapi.fmc.FMC')
    def test_PREFIX_URL_7(self, mock_fmc, mock_log, *_):
        """
        Test PREFIX_URL property
            - Category param
            - insertBefore param
            - insertAfter param
        """
        a = api_objects.ACPRule(fmc=mock_fmc, acp_name='something')
        a.category = 'something'
        a.insertBefore = 'something'
        a.insertAfter = 'something'

        self.assertEqual('/policy/accesspolicies?category=something&insertBefore=something&insertAfter=something',
                         a.PREFIX_URL)
        mock_log.assert_called_once()
