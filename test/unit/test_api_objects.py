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

    @mock.patch('fmcapi.api_objects.ACPRule.parse_kwargs')
    @mock.patch('fmcapi.fmc.FMC')
    def test_URL_SUFFIX_1(self, mock_fmc, *_):
        """
        Test URL_SUFFIX property
            - No URL params
        """
        a = api_objects.ACPRule(fmc=mock_fmc, acp_name='something')

        self.assertEqual('', a.URL_SUFFIX)

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    @mock.patch('fmcapi.api_objects.ACPRule.acp')
    @mock.patch('fmcapi.fmc.FMC')
    def test_URL_SUFFIX_2(self, mock_fmc, *_):
        """
        Test URL_SUFFIX property
            - Category param
        """
        a = api_objects.ACPRule(fmc=mock_fmc, acp_name='something', category='something')

        self.assertTrue(a.URL.endswith('?category=something'))

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    @mock.patch('fmcapi.api_objects.ACPRule.acp')
    @mock.patch('fmcapi.fmc.FMC')
    def test_URL_SUFFIX_3(self, mock_fmc, *_):
        """
        Test URL_SUFFIX property
            - insertBefore param
        """
        a = api_objects.ACPRule(fmc=mock_fmc, acp_name='something', insertBefore='something')

        self.assertTrue(a.URL.endswith('?insertBefore=something'))

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    @mock.patch('fmcapi.api_objects.ACPRule.acp')
    @mock.patch('fmcapi.fmc.FMC')
    def test_URL_SUFFIX_4(self, mock_fmc, *_):
        """
        Test URL_SUFFIX property
            - insertAfter param
        """
        a = api_objects.ACPRule(fmc=mock_fmc, acp_name='something', insertAfter='something')

        self.assertTrue(a.URL.endswith('?insertAfter=something'))

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    @mock.patch('fmcapi.api_objects.ACPRule.acp')
    @mock.patch('fmcapi.fmc.FMC')
    def test_URL_SUFFIX_5(self, mock_fmc, *_):
        """
        Test URL_SUFFIX property
            - category param
            - insertBefore param
        """
        a = api_objects.ACPRule(fmc=mock_fmc, acp_name='something', category='something', insertBefore='something')

        self.assertTrue(a.URL.endswith('?category=something&insertBefore=something'))

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    @mock.patch('fmcapi.api_objects.ACPRule.acp')
    @mock.patch('fmcapi.fmc.FMC')
    def test_URL_SUFFIX_6(self, mock_fmc, *_):
        """
        Test URL_SUFFIX property
            - Category param
            - insertAfter param
        """
        a = api_objects.ACPRule(fmc=mock_fmc, acp_name='something', category='something', insertAfter='something')

        self.assertTrue(a.URL.endswith('?category=something&insertAfter=something'))

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    @mock.patch('fmcapi.api_objects.ACPRule.acp')
    @mock.patch('logging.warning')
    @mock.patch('fmcapi.fmc.FMC')
    def test_URL_SUFFIX_7(self, mock_fmc, mock_log, *_):
        """
        Test URL_SUFFIX property
            - Category param
            - insertBefore param
            - insertAfter param
        """
        a = api_objects.ACPRule(fmc=mock_fmc,
                                acp_name='something',
                                category='something',
                                insertBefore='something',
                                insertAfter='something')

        self.assertTrue(a.URL.endswith('?category=something&insertBefore=something&insertAfter=something'))
        mock_log.assert_called_once()
