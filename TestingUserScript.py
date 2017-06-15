"""
Unit testing, of a sort, all the created methods/classes.
"""
import json
from fmcapi import *
import logging
import time

host = '192.168.11.5'
username = 'apiscript'
password = 'Admin123'
autodeploy = False

with FMC(host=host, username=username, password=password, autodeploy=autodeploy) as fmc1:
    '''Note:  I'd like to be able to test a name with bad characters but I haven't figured out how to use the
     "setter" decorator for this usecase yet.'''
    logging.info('# ### Mega Test Start!!! ### #')
    namer = '_fmcapi_test_{}'.format(str(int(time.time())))
    obj1 = None

    logging.info('# Testing URLGroup class.')
    url1 = URL(fmc=fmc1, name='_url1', url='example.org')
    url1.post()
    url2 = URL(fmc=fmc1, name='_url2', url='example.net')
    url2.post()
    url3 = URL(fmc=fmc1, name='_url3', url='example.com')
    url3.post()
    time.sleep(1)
    del obj1
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

    logging.info('# Testing NetworkGroup class.')
    obj10 = IPHost(fmc=fmc1, name='_iphost1', value='3.3.3.3')
    obj10.post()
    obj11 = IPNetwork(fmc=fmc1, name='_ipnet1', value='3.3.3.0/24')
    obj11.post()
    obj12 = IPRange(fmc=fmc1, name='_iprange1', value='3.3.3.3-33.33.33.33')
    obj12.post()
    time.sleep(1)
    del obj1
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

    logging.info('# Testing fmc.version() method.  Getting version information information from FMC.')
    version_info = fmc1.version()
    print(version_info)
    logging.info('# Testing fmc.verson() done.')

    logging.info('# Test IPAddresses.  This only returns a full list of Host/Network/Range objects.')
    del obj1
    obj1 = IPAddresses(fmc=fmc1)
    response = obj1.get()
    print(json.dumps(response))
    logging.info('# Test IPAddresses done.\n')

    logging.info('# Test VariableSet. Can only GET VariableSet objects.')
    del obj1
    obj1 = VariableSet(fmc=fmc1)
    obj1.get(name='Default-Set')
    print(json.dumps(obj1.format_data()))
    logging.info('# Test VariableSet done.\n')

    logging.info('# Test IPHost.  Post, get, put, delete Host Objects.')
    del obj1
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

    logging.info('# Test IPNetwork.  Post, get, put, delete Network Objects.')
    del obj1
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

    logging.info('# Test IPRange.  Post, get, put, delete Range Objects.')
    del obj1
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

    logging.info('# Test URL.  Post, get, put, delete URL Objects.')
    del obj1
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

    logging.info('# Test VlanTag.  Post, get, put, delete VLAN Tag Objects.')
    del obj1
    obj1 = VlanTag(fmc=fmc1)
    obj1.name = namer
    obj1.vlans(start_vlan='100', end_vlan='200')
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = VlanTag(fmc=fmc1, name=namer)
    obj1.get()
    obj1.vlans(start_vlan='300', end_vlan='400')
    obj1.put()
    time.sleep(1)
    obj1.delete()
    logging.info('# Test VlanTag done.\n')

    logging.info('# Test ProtocolPort.  Post, get, put, delete Port Objects.')
    del obj1
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

    logging.info('# Test SecurityZone.  Post, get, put, delete Security Zone Objects.')
    del obj1
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

    logging.info('# Test Device.  Though you can "Post" devices I do not have one handy. So '
                 'add/remove licenses on Device Objects.')
    del obj1
    obj1 = Device(fmc=fmc1)
    obj1.name = namer
    obj1.acp(name='Example_Corp')
    obj1.licensing(action='add', name='MALWARE')
    obj1.licensing(action='add', name='VPN')
    obj1.licensing(action='remove', name='VPN')
    obj1.licensing(action='clear')
    obj1.licensing(action='add', name='BASE')
    print(json.dumps(obj1.format_data()))
    logging.info('# Test Device done.\n')

    logging.info('# Test ItrusionPolicy. Can only GET IntrusionPolicy objects.')
    del obj1
    obj1 = IntrusionPolicy(fmc=fmc1)
    obj1.get(name='Security Over Connectivity')
    print(json.dumps(obj1.format_data()))
    logging.info('# Test IntrusionPolicy done.\n')

    logging.info('# Test AccessControlPolicy.  Post, get, put, delete ACP Objects.')
    del obj1
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

    logging.info('\n# In preparation for testing ACPRule methods, set up some known objects in the FMC.')
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
    
    logging.info('\n# Cleanup of testing ACPRule methods.')
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

    logging.info('# ### Mega Test Done!!! ### #')
