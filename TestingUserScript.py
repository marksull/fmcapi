"""
Unit testing, of a sort, all the created methods/classes.
"""
# import json
from fmcapi import *
import logging
import time
import pprint

# ### Set these variables to match your environment. ### #
host = '192.168.11.5'
username = 'apiscript'
password = 'Admin123'
autodeploy = False

# ### These functions are the individual tests you can run to ensure functionality. ### #


def test__url_category():
    logging.info('# Testing URLCategory class.')
    obj1 = URLCategory(fmc=fmc1)
    print('All URLCategories -- >')
    result = obj1.get()
    pp.pprint(result)
    print("Total items: {}".format(len(result['items'])))
    print('\n')
    del obj1
    obj1 = URLCategory(fmc=fmc1, name='SPAM URLs')
    print('One URLCategory -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing URLCategory class done.\n')


def test__ports():
    logging.info('# Test Ports.  This only returns a full list of various Port object types.')
    obj1 = Ports(fmc=fmc1)
    print('Ports -->')
    result = obj1.get()
    pp.pprint(result)
    print('\n')
    logging.info('# Test Ports done.\n')


def test__application_type():
    logging.info('# Testing ApplicationType class.')
    obj1 = ApplicationType(fmc=fmc1)
    print('All ApplicationType -- >')
    result = obj1.get()
    pp.pprint(result)
    print("Total items: {}".format(len(result['items'])))
    print('\n')
    del obj1
    obj1 = ApplicationType(fmc=fmc1, name='Server')
    print('One ApplicationType -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing ApplicationType class done.\n')


def test__application_tag():
    logging.info('# Testing ApplicationTag class.')
    obj1 = ApplicationTag(fmc=fmc1)
    print('All ApplicationTag -- >')
    result = obj1.get()
    pp.pprint(result)
    print("Total items: {}".format(len(result['items'])))
    print('\n')
    del obj1
    obj1 = ApplicationTag(fmc=fmc1, name='file sharing/transfer')
    print('One ApplicationTag -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing ApplicationTag class done.\n')


def test__application():
    logging.info('# Testing Application class.')
    obj1 = Application(fmc=fmc1)
    print('### Warning, this query takes a LONG time to process.  Watch the output.log file for regular updates. ###')
    print('All Application -- >')
    result = obj1.get()
    pp.pprint(result)
    print("Total items: {}".format(len(result['items'])))
    print('\n')
    del obj1
    obj1 = Application(fmc=fmc1, name='WD softwares Download/Update')
    print('### Warning, this query takes a LONG time to process.  Watch the output.log file for regular updates. ###')
    print('One Application -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing Application class done.\n')


def test__application_risk():
    logging.info('# Testing ApplicationRisk class.')
    obj1 = ApplicationRisk(fmc=fmc1)
    print('All ApplicationRisks -- >')
    result = obj1.get()
    pp.pprint(result)
    print("Total items: {}".format(len(result['items'])))
    print('\n')
    del obj1
    obj1 = ApplicationRisk(fmc=fmc1, name='Very High')
    print('One ApplicationRisk -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing ApplicationRisk class done.\n')


def test__application_productivity():
    logging.info('# Testing ApplicationProductivity class.')
    obj1 = ApplicationProductivity(fmc=fmc1)
    print('All ApplicationProductivities -- >')
    result = obj1.get()
    pp.pprint(result)
    print("Total items: {}".format(len(result['items'])))
    print('\n')
    del obj1
    obj1 = ApplicationProductivity(fmc=fmc1, name='Very Low')
    print('One ApplicationProductivity -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing ApplicationProductivity class done.\n')


def test__application_category():
    logging.info('# Testing ApplicationCategory class.')
    obj1 = ApplicationCategory(fmc=fmc1)
    print('All ApplicationCategories -- >')
    result = obj1.get()
    pp.pprint(result)
    print("Total items: {}".format(len(result['items'])))
    print('\n')
    del obj1
    obj1 = ApplicationCategory(fmc=fmc1, name='SMS tools')
    print('One ApplicationCategory -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing ApplicationCategory class done.\n')


def test__country():
    logging.info('# Testing Country class.')
    obj1 = Country(fmc=fmc1)
    print('All Countries -- >')
    result = obj1.get()
    pp.pprint(result)
    print("Total items: {}".format(len(result['items'])))
    print('\n')
    del obj1
    obj1 = Country(fmc=fmc1, name='Isle Of Man')
    print('One Country -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing Country class done.\n')


def test__continent():
    logging.info('# Testing Continent class.')
    obj1 = Continent(fmc=fmc1)
    print('All Continents -- >')
    result = obj1.get()
    pp.pprint(result)
    print("Total items: {}".format(len(result['items'])))
    print('\n')
    del obj1
    obj1 = Continent(fmc=fmc1, name='North America')
    print('One Continent -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing Continent class done.\n')


def test__vlan_group_tag():
    logging.info('# Testing VlanGroupTag class.')
    obj10 = VlanTag(fmc=fmc1, name='_vlantag10', data={'startTag': '888', 'endTag': '999'})
    obj10.post()
    obj11 = VlanTag(fmc=fmc1, name='_vlantag11', data={'startTag': '222', 'endTag': '333'})
    obj11.post()
    obj12 = VlanTag(fmc=fmc1, name='_vlantag12', data={'startTag': '1', 'endTag': '999'})
    obj12.post()
    time.sleep(1)
    obj1 = VlanGroupTag(fmc=fmc1, name=namer)
    obj1.named_vlantags(action='add', name='_vlantag10')
    obj1.named_vlantags(action='add', name='_vlantag11')
    obj1.named_vlantags(action='remove', name='_vlantag10')
    obj1.named_vlantags(action='clear')
    obj1.named_vlantags(action='add', name='_vlantag10')
    obj1.named_vlantags(action='add', name='_vlantag11')
    obj1.named_vlantags(action='add', name='_vlantag12')
    obj1.named_vlantags(action='remove', name='_vlantag12')
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = VlanGroupTag(fmc=fmc1, name=namer)
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


def test__url_group():
    logging.info('# Testing URLGroup class.')
    url1 = URL(fmc=fmc1, name='_url1', url='example.org')
    url1.post()
    url2 = URL(fmc=fmc1, name='_url2', url='example.net')
    url2.post()
    url3 = URL(fmc=fmc1, name='_url3', url='example.com')
    url3.post()
    time.sleep(1)
    obj1 = URLGroup(fmc=fmc1, name=namer)
    obj1.named_urls(action='add', name='_url1')
    obj1.named_urls(action='add', name='_url1')
    obj1.named_urls(action='clear')
    obj1.named_urls(action='add', name='_url2')
    obj1.named_urls(action='add', name='_url3')
    obj1.named_urls(action='add', name='_url1')
    obj1.named_urls(action='remove', name='_url3')
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = URLGroup(fmc=fmc1, name=namer)
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


def test__network_group():
    logging.info('# Testing NetworkGroup class.')
    obj10 = IPHost(fmc=fmc1, name='_iphost1', value='3.3.3.3')
    obj10.post()
    obj11 = IPNetwork(fmc=fmc1, name='_ipnet1', value='3.3.3.0/24')
    obj11.post()
    obj12 = IPRange(fmc=fmc1, name='_iprange1', value='3.3.3.3-33.33.33.33')
    obj12.post()
    time.sleep(1)
    obj1 = NetworkGroup(fmc=fmc1, name=namer)
    obj1.named_networks(action='add', name='_iphost1')
    obj1.named_networks(action='add', name='_iphost1')
    obj1.named_networks(action='remove', name='_iphost1')
    obj1.named_networks(action='clear')
    obj1.named_networks(action='add', name='_ipnet1')
    obj1.named_networks(action='add', name='_iprange1')
    obj1.named_networks(action='remove', name='_iphost1')
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = NetworkGroup(fmc=fmc1, name=namer)
    obj1.get()
    obj1.unnamed_networks(action='add', value='1.2.3.4')
    obj1.unnamed_networks(action='clear')
    obj1.unnamed_networks(action='add', value='1.2.3.4')
    obj1.unnamed_networks(action='remove', value='1.2.3.4')
    obj1.unnamed_networks(action='add', value='6.7.8.9')
    obj1.unnamed_networks(action='add', value='1.2.3.0/24')
    obj1.put()
    time.sleep(1)
    obj1.delete()
    obj10.delete()
    obj11.delete()
    obj12.delete()
    logging.info('# Testing NetworkGroup class done.\n')


def test__ip_addresses():
    logging.info('# Test IPAddresses.  This only returns a full list of IP object types.')
    obj1 = IPAddresses(fmc=fmc1)
    print('IPAddresses -->')
    result = obj1.get()
    pp.pprint(result)
    print('\n')
    logging.info('# Test IPAddresses done.\n')


def test__fmc_version():
    logging.info('# Testing fmc.version() method.  Getting version information information from FMC.')
    version_info = fmc1.version()
    print('fmc.version() -- >')
    pp.pprint(version_info)
    print('\n')
    logging.info('# Testing fmc.verson() done.')


def test__variable_set():
    logging.info('# Test VariableSet. Can only GET VariableSet objects.')
    obj1 = VariableSet(fmc=fmc1)
    obj1.get(name='Default-Set')
    print('VariableSet -->')
    pp.pprint(obj1.format_data())
    print('\n')
    logging.info('# Test VariableSet done.\n')


def test__ip_host():
    logging.info('# Test IPHost.  Post, get, put, delete Host Objects.')
    obj1 = IPHost(fmc=fmc1)
    obj1.name = namer
    obj1.value = '8.8.8.8/32'
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = IPHost(fmc=fmc1, name=namer)
    obj1.get()
    obj1.value = '9.9.9.9'
    obj1.put()
    time.sleep(1)
    obj1.delete()
    logging.info('# Test IPHost done.\n')


def test__ip_network():
    logging.info('# Test IPNetwork.  Post, get, put, delete Network Objects.')
    obj1 = IPNetwork(fmc=fmc1)
    obj1.name = namer
    obj1.value = '8.8.8.0/24'
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = IPNetwork(fmc=fmc1, name=namer)
    obj1.get()
    obj1.value = '9.9.9.0/24'
    obj1.put()
    time.sleep(1)
    obj1.delete()
    logging.info('# Test IPNetwork done.\n')


def test__ip_range():
    logging.info('# Test IPRange.  Post, get, put, delete Range Objects.')
    obj1 = IPRange(fmc=fmc1)
    obj1.name = namer
    obj1.value = '1.1.1.1-2.2.2.2'
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = IPRange(fmc=fmc1, name=namer)
    obj1.get()
    obj1.value = '3.3.3.3-4.4.4.4'
    obj1.put()
    time.sleep(1)
    obj1.delete()
    logging.info('# Test IPRange done.\n')


def test__url():
    logging.info('# Test URL.  Post, get, put, delete URL Objects.')
    obj1 = URL(fmc=fmc1)
    obj1.name = namer
    obj1.url = 'daxm.com'
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = URL(fmc=fmc1, name=namer)
    obj1.get()
    obj1.url = 'daxm.lan'
    obj1.put()
    time.sleep(1)
    obj1.delete()
    logging.info('# Test URL done.\n')


def test__vlan_tag():
    logging.info('# Test VlanTag.  Post, get, put, delete VLAN Tag Objects.')
    obj1 = VlanTag(fmc=fmc1)
    obj1.name = namer
    obj1.vlans(start_vlan='100', end_vlan='200')
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = VlanTag(fmc=fmc1, name=namer)
    obj1.get()
    obj1.vlans(start_vlan='400', end_vlan='300')
    obj1.put()
    time.sleep(1)
    obj1.delete()
    logging.info('# Test VlanTag done.\n')


def test__protocol_port():
    logging.info('# Test ProtocolPort.  Post, get, put, delete Port Objects.')
    obj1 = ProtocolPort(fmc=fmc1)
    obj1.name = namer
    obj1.port = '1234'
    obj1.protocol = 'TCP'
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = ProtocolPort(fmc=fmc1, name=namer)
    obj1.get()
    obj1.port = '5678'
    obj1.put()
    time.sleep(1)
    obj1.delete()
    logging.info('# Test ProtocolPort done.\n')


def test__security_zone():
    logging.info('# Test SecurityZone.  Post, get, put, delete Security Zone Objects.')
    obj1 = SecurityZone(fmc=fmc1)
    obj1.name = namer
    obj1.interfaceMode = 'ROUTED'
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = SecurityZone(fmc=fmc1, name=namer)
    obj1.get()
    obj1.name = 'DEMO'
    obj1.put()
    time.sleep(1)
    obj1.delete()
    logging.info('# Test SecurityZone done.\n')


def test__device():
    logging.info('# Test Device.  Though you can "Post" devices I do not have one handy. So '
                 'add/remove licenses on Device Objects.')
    obj1 = Device(fmc=fmc1)
    obj1.name = namer
    obj1.acp(name='Example_Corp')
    obj1.licensing(action='add', name='MALWARE')
    obj1.licensing(action='add', name='VPN')
    obj1.licensing(action='remove', name='VPN')
    obj1.licensing(action='clear')
    obj1.licensing(action='add', name='BASE')
    print('Device -->')
    pp.pprint(obj1.format_data())
    print('\n')
    logging.info('# Test Device done.\n')


def test__intrusion_policy():
    logging.info('# Test IntrusionPolicy. Can only GET IntrusionPolicy objects.')
    obj1 = IntrusionPolicy(fmc=fmc1)
    obj1.get(name='Security Over Connectivity')
    print('IntrusionPolicy -->')
    pp.pprint(obj1.format_data())
    print('\n')
    logging.info('# Test IntrusionPolicy done.\n')


def test__access_control_policy():
    logging.info('# Test AccessControlPolicy.  Post, get, put, delete ACP Objects.')
    obj1 = AccessControlPolicy(fmc=fmc1)
    obj1.name = namer
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = AccessControlPolicy(fmc=fmc1, name=namer)
    obj1.get()
    obj1.name = 'asdfasdf'
    obj1.put()
    time.sleep(1)
    obj1.delete()
    logging.info('# Test AccessControlPolicy done.\n')


def test__acp_rule():
    logging.info('# In preparation for testing ACPRule methods, set up some known objects in the FMC.')
    iphost1 = IPHost(fmc=fmc1, name='_iphost1', value='7.7.7.7')
    iphost1.post()
    ipnet1 = IPNetwork(fmc=fmc1, name='_ipnet1', value='1.2.3.0/24')
    ipnet1.post()
    iprange1 = IPRange(fmc=fmc1, name='_iprange1', value='6.6.6.6-7.7.7.7')
    iprange1.post()
    url1 = URL(fmc=fmc1, name='_url1', url='asdf.org')
    url1.post()
    vlantag1 = VlanTag(fmc=fmc1, name='_vlantag1', data={'startTag': '888', 'endTag': '999'})
    vlantag1.post()
    pport1 = ProtocolPort(fmc=fmc1, name='_pport1', port='9090', protocol='UDP')
    pport1.post()
    sz1 = SecurityZone(fmc=fmc1, name='_sz1', interfaceMode='ROUTED')
    sz1.post()
    acp1 = AccessControlPolicy(fmc=fmc1, name='_acp1')
    acp1.post()
    time.sleep(1)
    logging.info('# Setup of objects for ACPRule test done.\n')

    logging.info('# Test ACPRule.  Try to test all features of all methods of the ACPRule class.')
    acprule1 = ACPRule(fmc=fmc1, acp_name='_acp1')
    acprule1.name = '_acprule1'
    acprule1.action = 'ALLOW'
    acprule1.enabled = False
    acprule1.sendEventsToFMC = True
    acprule1.logFiles = False
    acprule1.logBegin = True
    acprule1.logEnd = True
    acprule1.variable_set(action='set', name='Default-Set')
    acprule1.source_zone(action='add', name='_sz1')
    acprule1.destination_zone(action='add', name='_sz1')
    acprule1.intrusion_policy(action='set', name='Security Over Connectivity')
    acprule1.vlan_tags(action='add', name='_vlantag1')
    acprule1.source_port(action='add', name='_pport1')
    acprule1.destination_port(action='add', name='_pport1')
    acprule1.source_network(action='add', name='_iphost1')
    acprule1.destination_network(action='add', name='_ipnet1')
    acprule1.source_network(action='add', name='_iprange1')
    acprule1.destination_network(action='add', name='_iprange1')
    acprule1.post()
    logging.info('# Test ACPRule done.\n')

    logging.info('# Cleanup of testing ACPRule methods.')
    acprule1.delete()
    time.sleep(1)
    iphost1.delete()
    ipnet1.delete()
    iprange1.delete()
    url1.delete()
    vlantag1.delete()
    pport1.delete()
    sz1.delete()
    acp1.delete()
    logging.info('# Cleanup of objects for ACPRule test done.\n')


def test__audit():
    logging.info('# Testing fmc.audit() method.')
    subsytem_list = [
        'Login',
        'Session Expiration',
        'Logout',
        'Objects > Object Management > SecurityZone',
        'API'
    ]
    endtime = str(int(time.time()))
    for subsystem in subsytem_list:
        print('fmc.audit() for {}. -->'.format(subsystem))
        pp.pprint(fmc1.audit(username=username, subsystem=subsystem, starttime=starttime, endtime=endtime))
        print('\n')
    logging.info('# Testing fmc.audit() method done.\n')

# ### Main Program ### #
with FMC(host=host, username=username, password=password, autodeploy=autodeploy) as fmc1:
    logging.info('# ### Mega Test Start!!! ### #')
    starttime = str(int(time.time()))
    namer = '_fmcapi_test_{}'.format(starttime)
    pp = pprint.PrettyPrinter(indent=4)

    test__url_category()
    test__ports()
    test__application_type()
    test__application_tag()
    test__application()
    test__application_risk()
    test__application_productivity()
    test__application_category()
    test__country()
    test__continent()
    test__vlan_group_tag()
    test__url_group()
    test__network_group()
    test__ip_addresses()
    test__fmc_version()
    test__variable_set()
    test__ip_host()
    test__ip_network()
    test__ip_range()
    test__url()
    test__vlan_tag()
    test__protocol_port()
    test__security_zone()
    test__device()
    test__intrusion_policy()
    test__access_control_policy()
    test__acp_rule()
    test__audit()
