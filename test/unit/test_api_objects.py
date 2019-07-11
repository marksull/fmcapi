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
        a = api_objects.ACPRule(fmc=mock_fmc, acp_name='something', category='something', insertBefore='something',
                                insertAfter='something')

        self.assertTrue(a.URL.endswith('?category=something&insertBefore=something&insertAfter=something'))
        mock_log.assert_called_once()

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    @mock.patch('fmcapi.api_objects.NetworkGroup')
    @mock.patch('fmcapi.api_objects.FQDNS')
    @mock.patch('fmcapi.api_objects.IPAddresses')
    def test_ACPRule_source_network_add_for_objects_and_no_objects_initially(self, mock_ipaddress, mock_fqdns, mock_nwgroup,
                                                                         _):
        value2 = mock.Mock()
        value = mock.Mock()
        value.get.return_value = value2
        dummyvalue3 = mock.Mock()
        dummyvalue4 = mock.Mock()
        dummyvalue4.get.return_value = []
        dummyvalue3.get.return_value = dummyvalue4
        value2.get.return_value = [
            {'name': 'someExistingObjectName1', 'id': 'someExistingObjectId1', 'type': 'someExistingObjectType1'},
            {'name': 'someExistingObjectName2', 'id': 'someExistingObjectId2', 'type': 'someExistingObjectType2'},
            {'name': 'someExistingObjectName3', 'id': 'someExistingObjectId3', 'type': 'someExistingObjectType3'}]
        mock_ipaddress.return_value = value
        mock_nwgroup.return_value = dummyvalue3
        mock_fqdns.return_value = dummyvalue3

        rule_obj = api_objects.ACPRule(fmc=mock.Mock())
        rule_obj.URL = '/accesspolicies/<accesspolicyid>/accessrules/<accessruleid>'
        rule_obj.source_network(action='add', name='someExistingObjectName2')
        self.assertEqual(len(rule_obj.sourceNetworks['objects']), 1)
        self.assertEqual(rule_obj.sourceNetworks, {'objects': [
            {'name': 'someExistingObjectName2', 'id': 'someExistingObjectId2', 'type': 'someExistingObjectType2'}]})

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    @mock.patch('fmcapi.api_objects.NetworkGroup')
    @mock.patch('fmcapi.api_objects.FQDNS')
    @mock.patch('fmcapi.api_objects.IPAddresses')
    def test_ACPRule_source_network_add_for_objects_and_one_objects_present_initially(self, mock_ipaddress, mock_fqdns,
                                                                                  mock_nwgroup, _):
        value2 = mock.Mock()
        value = mock.Mock()
        value.get.return_value = value2
        dummyvalue3 = mock.Mock()
        dummyvalue4 = mock.Mock()
        dummyvalue4.get.return_value = []
        dummyvalue3.get.return_value = dummyvalue4
        value2.get.return_value = [
            {'name': 'someExistingObjectName1', 'id': 'someExistingObjectId1', 'type': 'someExistingObjectType1'},
            {'name': 'someExistingObjectName2', 'id': 'someExistingObjectId2', 'type': 'someExistingObjectType2'},
            {'name': 'someExistingObjectName3', 'id': 'someExistingObjectId3', 'type': 'someExistingObjectType3'}]
        mock_ipaddress.return_value = value
        mock_nwgroup.return_value = dummyvalue3
        mock_fqdns.return_value = dummyvalue3
        rule_obj = api_objects.ACPRule(fmc=mock.Mock())
        rule_obj.sourceNetworks = {'objects': [
            {'name': 'someExistingObjectName3', 'id': 'someExistingObjectId3', 'type': 'someExistingObjectType3'}]}
        rule_obj.URL = '/accesspolicies/<accesspolicyid>/accessrules/<accessruleid>'
        rule_obj.source_network(action='add', name='someExistingObjectName2')
        self.assertEqual(len(rule_obj.sourceNetworks['objects']), 2)
        self.assertEqual(rule_obj.sourceNetworks['objects'][0],
                         {'name': 'someExistingObjectName3', 'id': 'someExistingObjectId3',
                          'type': 'someExistingObjectType3'})
        self.assertEqual(rule_obj.sourceNetworks['objects'][1],
                         {'name': 'someExistingObjectName2', 'id': 'someExistingObjectId2',
                          'type': 'someExistingObjectType2'})

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    @mock.patch('fmcapi.api_objects.NetworkGroup')
    @mock.patch('fmcapi.api_objects.FQDNS')
    @mock.patch('fmcapi.api_objects.IPAddresses')
    def test_ACPRule_source_network_add_for_objects_and_multiple_objects_present_initially(self, mock_ipaddress, mock_fqdns,
                                                                                       mock_nwgroup, _):
        value2 = mock.Mock()
        value = mock.Mock()
        value.get.return_value = value2
        dummyvalue3 = mock.Mock()
        dummyvalue4 = mock.Mock()
        dummyvalue4.get.return_value = []
        dummyvalue3.get.return_value = dummyvalue4
        value2.get.return_value = [
            {'name': 'someExistingObjectName1', 'id': 'someExistingObjectId1', 'type': 'someExistingObjectType1'},
            {'name': 'someExistingObjectName2', 'id': 'someExistingObjectId2', 'type': 'someExistingObjectType2'},
            {'name': 'someExistingObjectName3', 'id': 'someExistingObjectId3', 'type': 'someExistingObjectType3'}]
        mock_ipaddress.return_value = value
        mock_nwgroup.return_value = dummyvalue3
        mock_fqdns.return_value = dummyvalue3
        rule_obj = api_objects.ACPRule(fmc=mock.Mock())
        rule_obj.sourceNetworks = {'objects': [
            {'name': 'someExistingObjectName3', 'id': 'someExistingObjectId3', 'type': 'someExistingObjectType3'},
            {'name': 'someExistingObjectName1', 'id': 'someExistingObjectId1', 'type': 'someExistingObjectType1'}]}
        rule_obj.URL = '/accesspolicies/<accesspolicyid>/accessrules/<accessruleid>'
        rule_obj.source_network(action='add', name='someExistingObjectName2')
        self.assertEqual(len(rule_obj.sourceNetworks['objects']), 3)
        self.assertEqual(rule_obj.sourceNetworks['objects'][0],
                         {'name': 'someExistingObjectName3', 'id': 'someExistingObjectId3',
                          'type': 'someExistingObjectType3'})
        self.assertEqual(rule_obj.sourceNetworks['objects'][1],
                         {'name': 'someExistingObjectName1', 'id': 'someExistingObjectId1',
                          'type': 'someExistingObjectType1'})
        self.assertEqual(rule_obj.sourceNetworks['objects'][2],
                         {'name': 'someExistingObjectName2', 'id': 'someExistingObjectId2',
                          'type': 'someExistingObjectType2'})

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    @mock.patch('fmcapi.api_objects.NetworkGroup')
    @mock.patch('fmcapi.api_objects.FQDNS')
    @mock.patch('fmcapi.api_objects.IPAddresses')
    def test_ACPRule_source_network_add_for_objects_and_duplicate_objects_present(self, mock_ipaddress, mock_fqdns,
                                                                              mock_nwgroup, _):
        value2 = mock.Mock()
        value = mock.Mock()
        value.get.return_value = value2
        dummyvalue3 = mock.Mock()
        dummyvalue4 = mock.Mock()
        dummyvalue4.get.return_value = []
        dummyvalue3.get.return_value = dummyvalue4
        value2.get.return_value = [
            {'name': 'someExistingObjectName1', 'id': 'someExistingObjectId1', 'type': 'someExistingObjectType1'},
            {'name': 'someExistingObjectName2', 'id': 'someExistingObjectId2', 'type': 'someExistingObjectType2'},
            {'name': 'someExistingObjectName3', 'id': 'someExistingObjectId3', 'type': 'someExistingObjectType3'}]
        mock_ipaddress.return_value = value
        mock_nwgroup.return_value = dummyvalue3
        mock_fqdns.return_value = dummyvalue3
        rule_obj = api_objects.ACPRule(fmc=mock.Mock())
        rule_obj.sourceNetworks = {'objects': [
            {'name': 'someExistingObjectName3', 'id': 'someExistingObjectId3', 'type': 'someExistingObjectType3'},
            {'name': 'someExistingObjectName1', 'id': 'someExistingObjectId1', 'type': 'someExistingObjectType1'}]}
        rule_obj.URL = '/accesspolicies/<accesspolicyid>/accessrules/<accessruleid>'
        rule_obj.source_network(action='add', name='someExistingObjectName3')
        self.assertEqual(len(rule_obj.sourceNetworks['objects']), 2)
        self.assertEqual(rule_obj.sourceNetworks['objects'][0],
                         {'name': 'someExistingObjectName3', 'id': 'someExistingObjectId3',
                          'type': 'someExistingObjectType3'})
        self.assertEqual(rule_obj.sourceNetworks['objects'][1],
                         {'name': 'someExistingObjectName1', 'id': 'someExistingObjectId1',
                          'type': 'someExistingObjectType1'})

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    def test_ACPRule_source_network_add_for_literals_and_no_literal_present_initially(self, _):
        rule_obj = api_objects.ACPRule(fmc=mock.Mock())
        # rule_obj.sourceNetworks = {'objects': [
        #     {'name': 'someExistingObjectName3', 'id': 'someExistingObjectId3', 'type': 'someExistingObjectType3'},
        #     {'name': 'someExistingObjectName1', 'id': 'someExistingObjectId1', 'type': 'someExistingObjectType1'}]}
        rule_obj.URL = '/accesspolicies/<accesspolicyid>/accessrules/<accessruleid>'
        rule_obj.source_network(action='add', literal={'type': 'someLiteralType', 'value': 'someLiteralValue1'})
        self.assertEqual(len(rule_obj.sourceNetworks['literals']), 1)
        self.assertEqual(rule_obj.sourceNetworks['literals'][0],
                         {'type': 'someLiteralType', 'value': 'someLiteralValue1'})

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    def test_ACPRule_source_network_add_for_literals_and_one_literal_present_initially(self, _):
        rule_obj = api_objects.ACPRule(fmc=mock.Mock())
        rule_obj.sourceNetworks = {'literals': [{'type': 'someLiteralType', 'value': 'someLiteralValue2'}]}
        rule_obj.URL = '/accesspolicies/<accesspolicyid>/accessrules/<accessruleid>'
        rule_obj.source_network(action='add', literal={'type': 'someLiteralType', 'value': 'someLiteralValue1'})
        self.assertEqual(len(rule_obj.sourceNetworks['literals']), 2)
        self.assertEqual(rule_obj.sourceNetworks['literals'][0],
                         {'type': 'someLiteralType', 'value': 'someLiteralValue2'})
        self.assertEqual(rule_obj.sourceNetworks['literals'][1],
                         {'type': 'someLiteralType', 'value': 'someLiteralValue1'})

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    def test_ACPRule_source_network_add_for_literals_and_multiple_literal_present_initially(self, _):
        rule_obj = api_objects.ACPRule(fmc=mock.Mock())
        rule_obj.sourceNetworks = {'literals': [{'type': 'someLiteralType', 'value': 'someLiteralValue2'},
            {'type': 'someLiteralType', 'value': 'someLiteralValue3'},
            {'type': 'someLiteralType', 'value': 'someLiteralValue4'}]}
        rule_obj.URL = '/accesspolicies/<accesspolicyid>/accessrules/<accessruleid>'
        rule_obj.source_network(action='add', literal={'type': 'someLiteralType', 'value': 'someLiteralValue1'})
        self.assertEqual(len(rule_obj.sourceNetworks['literals']), 4)
        self.assertEqual(rule_obj.sourceNetworks['literals'][0],
                         {'type': 'someLiteralType', 'value': 'someLiteralValue2'})
        self.assertEqual(rule_obj.sourceNetworks['literals'][1],
                         {'type': 'someLiteralType', 'value': 'someLiteralValue3'})
        self.assertEqual(rule_obj.sourceNetworks['literals'][2],
                         {'type': 'someLiteralType', 'value': 'someLiteralValue4'})
        self.assertEqual(rule_obj.sourceNetworks['literals'][3],
                         {'type': 'someLiteralType', 'value': 'someLiteralValue1'})

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    def test_ACPRule_source_network_add_for_literals_and_duplicate_literal_present(self, _):
        rule_obj = api_objects.ACPRule(fmc=mock.Mock())
        rule_obj.sourceNetworks = {'literals': [{'type': 'someLiteralType', 'value': 'someLiteralValue2'},
            {'type': 'someLiteralType', 'value': 'someLiteralValue3'},
            {'type': 'someLiteralType', 'value': 'someLiteralValue4'}]}
        rule_obj.URL = '/accesspolicies/<accesspolicyid>/accessrules/<accessruleid>'
        rule_obj.source_network(action='add', literal={'type': 'someLiteralType', 'value': 'someLiteralValue4'})
        self.assertEqual(len(rule_obj.sourceNetworks['literals']), 3)
        self.assertEqual(rule_obj.sourceNetworks['literals'][0],
                         {'type': 'someLiteralType', 'value': 'someLiteralValue2'})
        self.assertEqual(rule_obj.sourceNetworks['literals'][1],
                         {'type': 'someLiteralType', 'value': 'someLiteralValue3'})
        self.assertEqual(rule_obj.sourceNetworks['literals'][2],
                         {'type': 'someLiteralType', 'value': 'someLiteralValue4'})

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    def test_ACPRule_source_network_add_for_literals_and_objects_present_initially(self, _):
        rule_obj = api_objects.ACPRule(fmc=mock.Mock())
        rule_obj.sourceNetworks = {'objects': [
            {'name': 'someExistingObjectName3', 'id': 'someExistingObjectId3', 'type': 'someExistingObjectType3'},
            {'name': 'someExistingObjectName1', 'id': 'someExistingObjectId1', 'type': 'someExistingObjectType1'}]}
        rule_obj.URL = '/accesspolicies/<accesspolicyid>/accessrules/<accessruleid>'
        rule_obj.source_network(action='add', literal={'type': 'someLiteralType', 'value': 'someLiteralValue4'})
        self.assertEqual(len(rule_obj.sourceNetworks['literals']), 1)
        self.assertEqual(rule_obj.sourceNetworks['literals'][0],
                         {'type': 'someLiteralType', 'value': 'someLiteralValue4'})
        self.assertEqual(rule_obj.sourceNetworks['objects'][0],
                         {'name': 'someExistingObjectName3', 'id': 'someExistingObjectId3',
                          'type': 'someExistingObjectType3'})
        self.assertEqual(rule_obj.sourceNetworks['objects'][1],
                         {'name': 'someExistingObjectName1', 'id': 'someExistingObjectId1',
                          'type': 'someExistingObjectType1'})

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    @mock.patch('fmcapi.api_objects.NetworkGroup')
    @mock.patch('fmcapi.api_objects.FQDNS')
    @mock.patch('fmcapi.api_objects.IPAddresses')
    def test_ACPRule_source_network_add_for_objects_and_literals_present_initially(self, mock_ipaddress, mock_fqdns,
                                                                              mock_nwgroup, _):
        value2 = mock.Mock()
        value = mock.Mock()
        value.get.return_value = value2
        dummyvalue3 = mock.Mock()
        dummyvalue4 = mock.Mock()
        dummyvalue4.get.return_value = []
        dummyvalue3.get.return_value = dummyvalue4
        value2.get.return_value = [
            {'name': 'someExistingObjectName1', 'id': 'someExistingObjectId1', 'type': 'someExistingObjectType1'},
            {'name': 'someExistingObjectName2', 'id': 'someExistingObjectId2', 'type': 'someExistingObjectType2'},
            {'name': 'someExistingObjectName3', 'id': 'someExistingObjectId3', 'type': 'someExistingObjectType3'}]
        mock_ipaddress.return_value = value
        mock_nwgroup.return_value = dummyvalue3
        mock_fqdns.return_value = dummyvalue3
        rule_obj = api_objects.ACPRule(fmc=mock.Mock())
        rule_obj.sourceNetworks = {'literals': [{'type': 'someLiteralType', 'value': 'someLiteralValue2'},
            {'type': 'someLiteralType', 'value': 'someLiteralValue3'},
            {'type': 'someLiteralType', 'value': 'someLiteralValue4'}]}
        rule_obj.URL = '/accesspolicies/<accesspolicyid>/accessrules/<accessruleid>'
        rule_obj.source_network(action='add', name='someExistingObjectName3')
        self.assertEqual(len(rule_obj.sourceNetworks['objects']), 1)
        self.assertEqual(rule_obj.sourceNetworks['objects'][0],
                         {'name': 'someExistingObjectName3', 'id': 'someExistingObjectId3',
                          'type': 'someExistingObjectType3'})
        self.assertEqual(len(rule_obj.sourceNetworks['literals']), 3)
        self.assertEqual(rule_obj.sourceNetworks['literals'][0],
                         {'type': 'someLiteralType', 'value': 'someLiteralValue2'})
        self.assertEqual(rule_obj.sourceNetworks['literals'][1],
                         {'type': 'someLiteralType', 'value': 'someLiteralValue3'})
        self.assertEqual(rule_obj.sourceNetworks['literals'][2],
                         {'type': 'someLiteralType', 'value': 'someLiteralValue4'})

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    def test_ACPRule_source_network_with_both_name_and_literals_given(self, _):
        rule_obj = api_objects.ACPRule(fmc=mock.Mock())
        with self.assertRaises(ValueError):
            rule_obj.source_network(action='add', name='someObjectName', literal={'type':'someType', 'value':'someValue'})

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    def test_ACPRule_source_network_remove_for_literals_with_multiple_literals_present(self, _):
        rule_obj = api_objects.ACPRule(fmc=mock.Mock())
        rule_obj.sourceNetworks = {'literals': [
            {'type': 'someLiteralType', 'value': 'someLiteralValue2'},
            {'type': 'someLiteralType', 'value': 'someLiteralValue3'},
            {'type': 'someLiteralType', 'value': 'someLiteralValue4'}]
        }
        rule_obj.source_network(action='remove', literal={'value':'someLiteralValue3'})
        self.assertEqual(len(rule_obj.sourceNetworks['literals']), 2)
        self.assertEqual(rule_obj.sourceNetworks['literals'][0],
                         {'type': 'someLiteralType', 'value': 'someLiteralValue2'})
        self.assertEqual(rule_obj.sourceNetworks['literals'][1],
                         {'type': 'someLiteralType', 'value': 'someLiteralValue4'})

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    def test_ACPRule_source_network_remove_for_literals_with_only_one_literal_present(self, _):
        rule_obj = api_objects.ACPRule(fmc=mock.Mock())
        rule_obj.sourceNetworks = {'literals': [
            {'type': 'someLiteralType', 'value': 'someLiteralValue2'}]
        }
        rule_obj.source_network(action='remove', literal={'value':'someLiteralValue2'})
        self.assertNotIn('sourceNetworks', self.__dict__)

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    def test_ACPRule_source_network_remove_for_objects_with_only_one_object_present(self, _):
        rule_obj = api_objects.ACPRule(fmc=mock.Mock())
        rule_obj.sourceNetworks = {'objects': [
            {'name': 'someExistingObjectName1', 'id': 'someExistingObjectId1', 'type': 'someExistingObjectType1'}]
        }
        rule_obj.source_network(action='remove', name='someExistingObjectName1')
        self.assertNotIn('sourceNetworks', self.__dict__)

    @mock.patch('fmcapi.api_objects.ACPRule.variable_set')
    def test_ACPRule_source_network_remove_for_objects_with_multiple_objects_present(self, _):
        rule_obj = api_objects.ACPRule(fmc=mock.Mock())
        rule_obj.sourceNetworks = {'objects': [
            {'name': 'someExistingObjectName1', 'id': 'someExistingObjectId1', 'type': 'someExistingObjectType1'},
            {'name': 'someExistingObjectName2', 'id': 'someExistingObjectId2', 'type': 'someExistingObjectType2'},
            {'name': 'someExistingObjectName3', 'id': 'someExistingObjectId3', 'type': 'someExistingObjectType3'}]
        }
        rule_obj.source_network(action='remove', name='someExistingObjectName3')
        self.assertEqual(len(rule_obj.sourceNetworks['objects']), 2)
        self.assertEqual(rule_obj.sourceNetworks['objects'][0],
                         {'name': 'someExistingObjectName1', 'id': 'someExistingObjectId1',
                          'type': 'someExistingObjectType1'})
        self.assertEqual(rule_obj.sourceNetworks['objects'][1],
                         {'name': 'someExistingObjectName2', 'id': 'someExistingObjectId2',
                          'type': 'someExistingObjectType2'})
