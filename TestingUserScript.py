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


def test__vlan_group_tag():
    logging.info('# Testing VlanGroupTag class.')
    obj10 = fmcapi.VlanTag(fmc=fmc1, name='_vlantag10', data={
                    'startTag': '888', 'endTag': '999'})
    obj10.post()
    obj11 = fmcapi.VlanTag(fmc=fmc1, name='_vlantag11', data={
                    'startTag': '222', 'endTag': '333'})
    obj11.post()
    obj12 = fmcapi.VlanTag(fmc=fmc1, name='_vlantag12', data={
                    'startTag': '1', 'endTag': '999'})
    obj12.post()
    time.sleep(1)
    obj1 = fmcapi.VlanGroupTag(fmc=fmc1, name=namer)
    obj1.named_vlantags(action='add', name=obj10.name)
    obj1.named_vlantags(action='add', name=obj11.name)
    obj1.named_vlantags(action='remove', name=obj11.name)
    obj1.named_vlantags(action='clear')
    obj1.named_vlantags(action='add', name=obj10.name)
    obj1.named_vlantags(action='add', name=obj11.name)
    obj1.named_vlantags(action='add', name=obj12.name)
    obj1.named_vlantags(action='remove', name=obj12.name)
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = fmcapi.VlanGroupTag(fmc=fmc1, name=namer)
    obj1.get()
    obj1.unnamed_vlantags(action='add', startvlan='22', endvlan='33')
    obj1.unnamed_vlantags(action='clear')
    obj1.unnamed_vlantags(action='add', startvlan='22', endvlan='33')
    obj1.unnamed_vlantags(action='remove', startvlan='22', endvlan='33')
    obj1.unnamed_vlantags(action='add', startvlan='44', endvlan='33')
    obj1.unnamed_vlantags(action='add', startvlan='900')
    obj1.put()
    time.sleep(1)
    obj1.delete()
    obj10.delete()
    obj11.delete()
    obj12.delete()
    logging.info('# Testing VlanGroupTag class done.\n')
    time.sleep(sleep_time_between_tests)


def test__url_group():
    logging.info('# Testing URLGroup class.')
    url1 = fmcapi.URL(fmc=fmc1, name='_url1', url='example.org')
    url1.post()
    url2 = fmcapi.URL(fmc=fmc1, name='_url2', url='example.net')
    url2.post()
    url3 = fmcapi.URL(fmc=fmc1, name='_url3', url='example.com')
    url3.post()
    time.sleep(1)
    obj1 = fmcapi.URLGroup(fmc=fmc1, name=namer)
    obj1.named_urls(action='add', name=url1.name)
    obj1.named_urls(action='add', name=url1.name)
    obj1.named_urls(action='clear')
    obj1.named_urls(action='add', name=url2.name)
    obj1.named_urls(action='add', name=url3.name)
    obj1.named_urls(action='add', name=url1.name)
    obj1.named_urls(action='remove', name=url3.name)
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = fmcapi.URLGroup(fmc=fmc1, name=namer)
    obj1.get()
    obj1.unnamed_urls(action='add', value='daxm.net')
    obj1.unnamed_urls(action='add', value='daxm.com')
    obj1.unnamed_urls(action='clear')
    obj1.unnamed_urls(action='add', value='daxm.org')
    obj1.unnamed_urls(action='add', value='daxm.net')
    obj1.unnamed_urls(action='add', value='daxm.lan')
    obj1.unnamed_urls(action='remove', value='daxm.org')
    obj1.put()
    time.sleep(1)
    obj1.delete()
    url1.delete()
    url2.delete()
    url3.delete()
    logging.info('# Testing URLGroup class done.\n')
    time.sleep(sleep_time_between_tests)


def test__network_group():
    logging.info('# Testing NetworkGroup class.')
    obj10 = fmcapi.IPHost(fmc=fmc1, name='_iphost1', value='3.3.3.3')
    obj10.post()
    obj11 = fmcapi.IPNetwork(fmc=fmc1, name='_ipnet1', value='3.3.3.0/24')
    obj11.post()
    obj12 = fmcapi.IPRange(fmc=fmc1, name='_iprange1', value='3.3.3.3-33.33.33.33')
    obj12.post()
    time.sleep(1)
    obj1 = fmcapi.NetworkGroup(fmc=fmc1, name=namer)
    obj1.named_networks(action='add', name=obj10.name)
    obj1.named_networks(action='add', name=obj10.name)
    obj1.named_networks(action='remove', name=obj10.name)
    obj1.named_networks(action='clear')
    obj1.named_networks(action='add', name=obj11.name)
    obj1.named_networks(action='add', name=obj12.name)
    obj1.named_networks(action='remove', name=obj11.name)
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = fmcapi.NetworkGroup(fmc=fmc1, name=namer)
    obj1.get()
    obj1.unnamed_networks(action='add', value='1.2.3.4')
    obj1.unnamed_networks(action='clear')
    obj1.unnamed_networks(action='add', value='1.2.3.4')
    obj1.unnamed_networks(action='remove', value='1.2.3.4')
    obj1.unnamed_networks(action='add', value='6.7.8.9')
    obj1.unnamed_networks(action='add', value='1.2.3.0/24')
    obj1.post()
    time.sleep(1)
    obj1.delete()
    obj10.delete()
    obj11.delete()
    obj12.delete()
    logging.info('# Testing NetworkGroup class done.\n')
    time.sleep(sleep_time_between_tests)


def test__ip_addresses():
    logging.info(
        '# Test IPAddresses.  This only returns a full list of IP object types.')
    obj1 = fmcapi.IPAddresses(fmc=fmc1)
    print('IPAddresses -->')
    result = obj1.get()
    pp.pprint(result)
    print('\n')
    logging.info('# Test IPAddresses done.\n')
    time.sleep(sleep_time_between_tests)


def test__fmc_version():
    logging.info(
        '# Testing fmc.version() method.  Getting version information information from FMC.')
    version_info = fmc1.version()
    print('fmc.version() -- >')
    pp.pprint(version_info)
    print('\n')
    logging.info('# Testing fmc.verson() done.')
    time.sleep(sleep_time_between_tests)


def test__variable_set():
    logging.info('# Test VariableSet. Can only GET VariableSet objects.')
    obj1 = fmcapi.VariableSet(fmc=fmc1)
    obj1.get(name='Default-Set')
    print('VariableSet -->')
    pp.pprint(obj1.format_data())
    print('\n')
    logging.info('# Test VariableSet done.\n')
    time.sleep(sleep_time_between_tests)


def test__ip_host():
    logging.info('# Test IPHost.  Post, get, put, delete Host Objects.')
    obj1 = fmcapi.IPHost(fmc=fmc1)
    obj1.name = namer
    obj1.value = '8.8.8.8/32'
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = fmcapi.IPHost(fmc=fmc1, name=namer)
    obj1.get()
    obj1.value = '9.9.9.9'
    obj1.put()
    time.sleep(1)
    obj1.delete()
    logging.info('# Test IPHost done.\n')
    time.sleep(sleep_time_between_tests)


def test__ip_network():
    logging.info('# Test IPNetwork.  Post, get, put, delete Network Objects.')
    obj1 = fmcapi.IPNetwork(fmc=fmc1)
    obj1.name = namer
    obj1.value = '8.8.8.0/24'
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = fmcapi.IPNetwork(fmc=fmc1, name=namer)
    obj1.get()
    obj1.value = '9.9.9.0/24'
    obj1.put()
    time.sleep(1)
    obj1.delete()
    logging.info('# Test IPNetwork done.\n')
    time.sleep(sleep_time_between_tests)


def test__ip_range():
    logging.info('# Test IPRange.  Post, get, put, delete Range Objects.')
    obj1 = fmcapi.IPRange(fmc=fmc1)
    obj1.name = namer
    obj1.value = '1.1.1.1-2.2.2.2'
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = fmcapi.IPRange(fmc=fmc1, name=namer)
    obj1.get()
    obj1.value = '3.3.3.3-4.4.4.4'
    obj1.put()
    time.sleep(1)
    obj1.delete()
    logging.info('# Test IPRange done.\n')
    time.sleep(sleep_time_between_tests)


def test__extended_acls():
    logging.info(
        '# Testing ExtendedAccessList class. Requires a configured ExtendedAccessList')
    obj1 = fmcapi.ExtendedAccessList(fmc=fmc1)
    print('All ExtendedAccessList -- >')
    result = obj1.get()
    pp.pprint(result)
    print(f"Total items: {len(result['items'])}")
    print('\n')
    del obj1
    obj1 = fmcapi.ExtendedAccessList(fmc=fmc1, name='_tmp')
    print('One ExtendedAccessList -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing ExtendedAccessList class done.\n')
    time.sleep(sleep_time_between_tests)


def test__geolocations():
    logging.info(
        '# Testing Geolocation class. Requires a configured Geolocation')
    obj1 = fmcapi.Geolocation(fmc=fmc1)
    print('All Geolocation -- >')
    result = obj1.get()
    pp.pprint(result)
    print(f"Total items: {len(result['items'])}")
    print('\n')
    del obj1
    obj1 = fmcapi.Geolocation(fmc=fmc1, name='_tmp')
    print('One Geolocation -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing Geolocation class done.\n')
    time.sleep(sleep_time_between_tests)


def test__icmpv4():
    logging.info(
        '# Test ICMPv4Object.  Post, get, put, delete ICMPv4Object Objects.')
    obj1 = fmcapi.ICMPv4Object(fmc=fmc1)
    obj1.name = "_icmpv4" + namer
    obj1.icmpType = "3"
    obj1.code = "0"
    obj1.post()

    obj1.get()
    obj1.code = "3"
    obj1.put()

    obj1.delete()
    logging.info('# FQDNS ICMPv4Object class done.\n')
    time.sleep(sleep_time_between_tests)


def test__icmpv6():
    logging.info(
        '# Test ICMPv6Object.  Post, get, put, delete ICMPv6Object Objects.')
    obj1 = fmcapi.ICMPv6Object(fmc=fmc1)
    obj1.name = "_icmpv6" + namer
    obj1.icmpType = "1"
    obj1.code = "0"
    obj1.post()

    obj1.get()
    obj1.code = "3"
    obj1.put()

    obj1.delete()
    logging.info('# FQDNS ICMPv6Object class done.\n')
    time.sleep(sleep_time_between_tests)


def test__ikev1():
    logging.info(
        '# Test IKEv1Policies and IKEv1IpsecProposals.'
        '  Post, get, put, delete IKEv1Policies and IKEv1IpsecProposals Objects.')
    ipsec1 = fmcapi.IKEv1IpsecProposals(fmc=fmc1)
    ipsec1.name = "_ipsec" + namer
    ipsec1.espEncryption = "AES-128"
    ipsec1.espHash = "SHA"
    ipsec1.post()

    ipsec1.get()
    ipsec1.espEncryption = "AES-192"
    ipsec1.put()

    pol1 = fmcapi.IKEv1Policies(fmc=fmc1)
    pol1.name = "_pol" + namer
    pol1.encryption = "3DES"
    pol1.hash = "SHA"
    pol1.priority = "10"
    pol1.diffieHellmanGroup = "5"
    pol1.authenticationMethod = "Preshared Key"
    pol1.lifetimeInSeconds = "3600"
    pol1.post()

    pol1.get()
    pol1.encryption = "AES-128"
    pol1.put()

    ipsec1.delete()
    pol1.delete()
    logging.info('# Test IKEv1Policies and IKEv1IpsecProposals classes done.\n')
    time.sleep(sleep_time_between_tests)


def test__ikev2():
    logging.info(
        '# Test IKEv2Policies and IKEv2IpsecProposals.'
        '  Post, get, put, delete IKEv2Policies and IKEv2IpsecProposals Objects.')
    encryption_list = ['AES', 'AES-192', 'AES-256', 'NULL']
    integrity_list1 = ['NULL', 'SHA-1', 'SHA-256', 'SHA-384', 'SHA-512']
    ipsec_integrity_list1 = ['NULL', 'SHA', 'SHA-256', 'SHA-384', 'SHA-512']
    # 'NULL' is invalid for prf_integrity.  Should generate a warning log and ignore that type.
    prf_integrity_list1 = ['NULL', 'SHA', 'SHA-256', 'SHA-384', 'SHA-512']

    ipsec1 = fmcapi.IKEv2IpsecProposals(fmc=fmc1)
    ipsec1.name = "_ipsec" + namer
    ipsec1.encryption(action='add', algorithms=encryption_list)
    ipsec1.hash(action='add', algorithms=integrity_list1)
    ipsec1.post()

    ipsec1.get()
    # Try to add a duplicate
    ipsec1.encryption(action='add', algorithms=['AES-192'])
    ipsec1.hash(action='add', algorithms=['SHA-1'])

    ipsec1.encryption(action='remove', algorithms=['NULL'])
    ipsec1.hash(action='remove', algorithms=['NULL'])
    ipsec1.put()

    # None of the algorithms can contain an empty list
    ipsec1.get()
    ipsec1.encryption(action='clear')
    ipsec1.hash(action='clear')
    ipsec1.encryption(action='add', algorithms=['AES-192'])
    ipsec1.hash(action='add', algorithms=['SHA-1'])
    ipsec1.put()

    pol1 = fmcapi.IKEv2Policies(fmc=fmc1)
    pol1.name = "_pol" + namer
    pol1.priority = "10"
    pol1.diffieHellmanGroups = ["2", "5"]
    pol1.encryption(action='add', algorithms=encryption_list)
    pol1.hash(action='add', algorithms=ipsec_integrity_list1)
    pol1.prf_hash(action='add', algorithms=prf_integrity_list1)
    pol1.lifetimeInSeconds = "3600"
    pol1.post()

    pol1.get()
    # Try to add a duplicate
    pol1.encryption(action='add', algorithms=['AES-192'])
    pol1.hash(action='add', algorithms=['NULL'])
    pol1.prf_hash(action='add', algorithms=['SHA'])

    pol1.encryption(action='remove', algorithms=['NULL'])
    pol1.hash(action='remove', algorithms=['NULL'])
    pol1.prf_hash(action='remove', algorithms=['SHA'])
    pol1.put()

    # None of the algorithms can contain an empty list
    pol1.get()
    pol1.encryption(action='clear')
    pol1.hash(action='clear')
    pol1.prf_hash(action='clear')
    pol1.encryption(action='add', algorithms=['AES-192'])
    pol1.hash(action='add', algorithms=['NULL'])
    pol1.prf_hash(action='add', algorithms=['SHA'])
    pol1.put()

    ipsec1.delete()
    pol1.delete()
    logging.info('# Test IKEv2Policies and IKEv2IpsecProposals classes done.\n')
    time.sleep(sleep_time_between_tests)


def test__url():
    logging.info('# Test URL.  Post, get, put, delete URL Objects.')
    obj1 = fmcapi.URL(fmc=fmc1)
    obj1.name = namer
    obj1.url = 'daxm.com'
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = fmcapi.URL(fmc=fmc1, name=namer)
    obj1.get()
    obj1.url = 'daxm.lan'
    obj1.put()
    time.sleep(1)
    obj1.delete()
    logging.info('# Test URL done.\n')
    time.sleep(sleep_time_between_tests)


def test__vlan_tag():
    logging.info('# Test VlanTag.  Post, get, put, delete VLAN Tag Objects.')
    obj1 = fmcapi.VlanTag(fmc=fmc1)
    obj1.name = namer
    obj1.vlans(start_vlan='100', end_vlan='200')
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = fmcapi.VlanTag(fmc=fmc1, name=namer)
    obj1.get()
    obj1.vlans(start_vlan='400', end_vlan='300')
    obj1.put()
    time.sleep(1)
    obj1.delete()
    logging.info('# Test VlanTag done.\n')
    time.sleep(sleep_time_between_tests)






# ### Main Program ### #


with fmcapi.FMC(host=host, username=username, password=password, autodeploy=autodeploy, limit=10) as fmc1:
    logging.info('# ### Mega Test Start!!! ### #')
    starttime = str(int(time.time()))
    namer = f'_fmcapi_test_{starttime}'
    pp = pprint.PrettyPrinter(indent=4)
    time.sleep(1)

    ''' 
    # Working Tests
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
