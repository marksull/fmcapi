"""
Unit testing, of a sort, all the created methods/classes.
"""

import fmcapi
import logging
import time
import pprint
import unit_tests


# ### Set these variables to match your environment. ### #

host = '10.0.0.10'
username = 'apiadmin'
password = 'Admin123'
autodeploy = False

sleep_time_between_tests = 1

# ### These functions are the individual tests you can run to ensure functionality. ### #


def test__application_type():
    logging.info('# Testing ApplicationType class.')
    obj1 = fmcapi.ApplicationType(fmc=fmc1)
    print('All ApplicationType -- >')
    result = obj1.get()
    pp.pprint(result)
    print(f"Total items: {len(result['items'])}")
    print('\n')
    del obj1
    obj1 = fmcapi.ApplicationType(fmc=fmc1, name='Server')
    print('One ApplicationType -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing ApplicationType class done.\n')
    time.sleep(sleep_time_between_tests)


def test__application_tag():
    logging.info('# Testing ApplicationTag class.')
    obj1 = fmcapi.ApplicationTag(fmc=fmc1)
    print('All ApplicationTag -- >')
    result = obj1.get()
    pp.pprint(result)
    print(f"Total items: {len(result['items'])}")
    print('\n')
    del obj1
    obj1 = fmcapi.ApplicationTag(fmc=fmc1, name='file sharing/transfer')
    print('One ApplicationTag -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing ApplicationTag class done.\n')
    time.sleep(sleep_time_between_tests)


def test__application():
    logging.info('# Testing Application class.')
    obj1 = fmcapi.Application(fmc=fmc1)
    print("### Warning, this query takes a LONG time to process if you don't increase the limit of the query set. ###")
    print('All Application -- >')
    result = obj1.get(limit=1000)
    pp.pprint(result)
    print(f"Total items: {len(result['items'])}")
    print('\n')
    del obj1
    obj1 = fmcapi.Application(fmc=fmc1, name='WD softwares Download/Update')
    print("### Warning, this query takes a LONG time to process if you don't increase the limit of the query set. ###")
    print('One Application -- >')
    pp.pprint(obj1.get(limit=1000))
    print('\n')
    logging.info('# Testing Application class done.\n')
    time.sleep(sleep_time_between_tests)


def test__application_risk():
    logging.info('# Testing ApplicationRisk class.')
    obj1 = fmcapi.ApplicationRisk(fmc=fmc1)
    print('All ApplicationRisks -- >')
    result = obj1.get()
    pp.pprint(result)
    print(f"Total items: {len(result['items'])}")
    print('\n')
    del obj1
    obj1 = fmcapi.ApplicationRisk(fmc=fmc1, name='Very High')
    print('One ApplicationRisk -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing ApplicationRisk class done.\n')
    time.sleep(sleep_time_between_tests)


def test__application_filter():
    logging.info('# Testing ApplicationFilter class.')
    obj1 = fmcapi.ApplicationFilter(fmc=fmc1)
    print('All ApplicationFilters -- >')
    result = obj1.get()
    pp.pprint(result)
    # There are no Application Filters by default so there is no items in the list.
    if 'items' in result:
        print(f"Total items: {len(result['items'])}")
        print('\n')
    del obj1
    logging.info('# Testing ApplicationFilter class done.\n')
    time.sleep(sleep_time_between_tests)


def test__application_productivity():
    logging.info('# Testing ApplicationProductivity class.')
    obj1 = fmcapi.ApplicationProductivity(fmc=fmc1)
    print('All ApplicationProductivities -- >')
    result = obj1.get()
    pp.pprint(result)
    print(f"Total items: {len(result['items'])}")
    print('\n')
    del obj1
    obj1 = fmcapi.ApplicationProductivity(fmc=fmc1, name='Very Low')
    print('One ApplicationProductivity -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing ApplicationProductivity class done.\n')
    time.sleep(sleep_time_between_tests)


def test__application_category():
    logging.info('# Testing ApplicationCategory class.')
    obj1 = fmcapi.ApplicationCategory(fmc=fmc1)
    print('All ApplicationCategories -- >')
    result = obj1.get()
    pp.pprint(result)
    print(f"Total items: {len(result['items'])}")
    print('\n')
    del obj1
    obj1 = fmcapi.ApplicationCategory(fmc=fmc1, name='SMS tools')
    print('One ApplicationCategory -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing ApplicationCategory class done.\n')
    time.sleep(sleep_time_between_tests)


def test__cert_enrollment():
    logging.info('# Testing CertEnrollment class. Requires a CertEnrollment')
    obj1 = fmcapi.CertEnrollment(fmc=fmc1)
    print('All CertEnrollments -- >')
    result = obj1.get()
    pp.pprint(result)
    print(f"Total items: {len(result['items'])}")
    print('\n')
    del obj1
    obj1 = fmcapi.CertEnrollment(fmc=fmc1, name='_tmp')
    print('One CertEnrollment -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing CertEnrollment class done.\n')
    time.sleep(sleep_time_between_tests)


def test__country():
    logging.info('# Testing Country class.')
    obj1 = fmcapi.Country(fmc=fmc1)
    print('All Countries -- >')
    result = obj1.get()
    pp.pprint(result)
    print(f"Total items: {len(result['items'])}")
    print('\n')
    del obj1
    obj1 = fmcapi.Country(fmc=fmc1, name='Isle Of Man')
    print('One Country -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing Country class done.\n')
    time.sleep(sleep_time_between_tests)


def test__filepolicies():
    logging.info('# Testing FilePolicies class.')
    obj1 = fmcapi.FilePolicies(fmc=fmc1)
    print('All FilePolicies -- >')
    result = obj1.get()
    pp.pprint(result)
    print(f"Total items: {len(result['items'])}")
    print('\n')
    del obj1
    logging.info('# Testing FilePolicies class done.\n')
    time.sleep(sleep_time_between_tests)


def test__continent():
    logging.info('# Testing Continent class.')
    obj1 = fmcapi.Continent(fmc=fmc1)
    print('All Continents -- >')
    result = obj1.get()
    pp.pprint(result)
    print(f"Total items: {len(result['items'])}")
    print('\n')
    del obj1
    obj1 = fmcapi.Continent(fmc=fmc1, name='North America')
    print('One Continent -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing Continent class done.\n')
    time.sleep(sleep_time_between_tests)


def test__dns_servers_group():
    logging.info(
        '# Test DNSServerGroups.  Post, get, put, delete DNSServerGroups Objects.')
    server_list = ["192.0.2.1", "192.0.2.2"]
    obj1 = fmcapi.DNSServerGroups(fmc=fmc1)
    obj1.name = "_dns1" + namer
    obj1.timeout = "3"
    obj1.defaultdomain = "cisco.com"
    obj1.post()

    obj1.get()
    obj1.servers(action='add', name_servers=server_list)
    obj1.put()

    obj1.delete()
    logging.info('# Testing DNSServerGroups class done.\n')
    time.sleep(sleep_time_between_tests)


def test__fqdns():
    logging.info(
        '# Test FQDNS.  Post, get, put, delete FQDNS Objects.')
    obj1 = fmcapi.FQDNS(fmc=fmc1)
    obj1.name = "_fqdns1" + namer
    obj1.value = "www.cisco.com"
    obj1.dnsResolution = "IPV4_ONLY"
    obj1.post()

    obj1.get()
    obj1.dnsResolution = "IPV4_AND_IPV6"
    obj1.put()

    obj1.delete()
    logging.info('# FQDNS DNSServerGroups class done.\n')
    time.sleep(sleep_time_between_tests)


with fmcapi.FMC(host=host, username=username, password=password, autodeploy=autodeploy, limit=10) as fmc1:
    logging.info('# ### Mega Test Start!!! ### #')
    starttime = str(int(time.time()))
    namer = f'_fmcapi_test_{starttime}'
    pp = pprint.PrettyPrinter(indent=4)
    print('')

    ''' 
    # Working Tests
    unit_tests.test__vlan_group_tag(fmc=fmc1)
    unit_tests.test__url_group(fmc=fmc1)
    unit_tests.test__network_group(fmc=fmc1)
    unit_tests.test__ip_addresses(fmc=fmc1)
    unit_tests.test__fmc_version(fmc=fmc1)
    unit_tests.test__variable_set(fmc=fmc1)
    unit_tests.test__ip_host(fmc=fmc1)
    unit_tests.test__ip_network(fmc=fmc1)
    unit_tests.test__ip_range(fmc=fmc1)
    unit_tests.test__extended_acls(fmc=fmc1)
    unit_tests.test__geolocations(fmc=fmc1)
    unit_tests.test__icmpv4(fmc=fmc1)
    unit_tests.test__icmpv6(fmc=fmc1)
    unit_tests.test__ikev1(fmc=fmc1)
    unit_tests.test__ikev2(fmc=fmc1)
    unit_tests.test__url(fmc=fmc1)
    unit_tests.test__vlan_tag(fmc=fmc1)
    unit_tests.test__protocol_port(fmc=fmc1)
    unit_tests.test__security_zone(fmc=fmc1)
    unit_tests.test__slamonitor(fmc=fmc1)
    unit_tests.test__intrusion_policy(fmc=fmc1)
    unit_tests.test__access_control_policy(fmc=fmc1)
    unit_tests.test__acp_rule(fmc=fmc1)
    unit_tests.test__audit(fmc=fmc1)
    unit_tests.test__port_object_group(fmc=fmc1)
    unit_tests.test__url_category(fmc=fmc1)
    unit_tests.test__ports(fmc=fmc1)
    '''

    '''
    # Not working tests
    unit_tests.test__static_routes(fmc=fmc1)
    unit_tests.test__ipv4_static_routes(fmc=fmc1)
    unit_tests.test__autonat(fmc=fmc1)  # Security Zones need to be created.
    unit_tests.test__manualnat(fmc=fmc1)  # Security Zones need to be created.
    unit_tests.test__upgrades(fmc=fmc1)

    # Need FTD device to test
    unit_tests.test__interface_group(fmc=fmc1)
    unit_tests.test__device(fmc=fmc1)
    unit_tests.test__device_with_task(fmc=fmc1)
    unit_tests.test__phys_interfaces(fmc=fmc1)
    unit_tests.test__redundant_interfaces(fmc=fmc1)
    unit_tests.test__etherchannel_interfaces(fmc=fmc1)
    unit_tests.test__subinterfaces(fmc=fmc1)
    unit_tests.test__device_group(fmc=fmc1)
    unit_tests.test__device_ha_monitored_interfaces(fmc=fmc1)
    unit_tests.test__device_ha_failover_mac(fmc=fmc1)
    unit_tests.test__device_ha_pair(fmc=fmc1)
    '''
