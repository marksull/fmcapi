"""
Just a rough working space for me to test running code against the fmcapi package.
"""

from fmcapi import *
import logging

host = '192.168.11.5'
username = 'apiscript'
password = 'Admin123'
autodeploy = False

with FMC(host=host, username=username, password=password, autodeploy=autodeploy) as fmc1:
    acp_rule1 = ACPRule(fmc=fmc1)
    acp_rule1.name = 'my_test_rule'
    acp_rule1.acp(name='Example_Corp')
    #print(acp_rule1.__dict__)
    #acp_rule1.post()

'''
    acp_rule1.source_port(action='add', name='AOL')
    acp_rule1.destination_port(action='add', name='AOL')
    acp_rule1.source_port(action='add', name='AOL')
    acp_rule1.destination_port(action='add', name='AOL')
    print(acp_rule1.__dict__)
    acp_rule1.destination_port(action='remove', name='AOL')
    acp_rule1.source_port(action='clear', name='')
    print(acp_rule1.__dict__)

    acp_rule1.vlan_tags(action='add', name='asdf')
    acp_rule1.vlan_tags(action='add', name='asdf')
    acp_rule1.vlan_tags(action='add', name='vlan1')
    print(acp_rule1.__dict__)
    acp_rule1.vlan_tags(action='remove', name='vlan1')
    print(acp_rule1.__dict__)
    acp_rule1.vlan_tags(action='clear', name='vlan1')
    print(acp_rule1.__dict__)

    vlan1 = VlanTag(fmc=fmc1, name='qwerty')
    vlan1.vlans(start_vlan=1, end_vlan=4094)
    vlan1.vlans(start_vlan=234, end_vlan=123)
    vlan1.vlans(start_vlan=1, end_vlan=4095)
    vlan1.vlans(start_vlan=0, end_vlan=4094)
    print(vlan1.__dict__)

    acp_rule1.source_zone(action='add', name='IN')
    acp_rule1.source_zone(action='add', name='IN')
    acp_rule1.source_zone(action='add', name='OUT')
    print(acp_rule1.__dict__)
    acp_rule1.source_zone(action='remove', name='OUT')
    print(acp_rule1.__dict__)
    acp_rule1.intrusion_policy(action='set', name='Connectivity Over Security')
    acp_rule1.variable_set(action='set')
    print(acp_rule1.__dict__)
    acp_rule1.variable_set(action='clear')
    acp_rule1.intrusion_policy(action='clear')
    print(acp_rule1.__dict__)

    device1 = Device(fmc=fmc1)
    device1.license_add()
    device1.license_add(license='VPN')
    print(device1.__dict__)
    device1.license_add(license='VPN')
    print(device1.__dict__)
    device1.license_add(license='MALWARE')
    print(device1.__dict__)
    device1.license_remove(license='MALWARE')
    print(device1.__dict__)
    device1.acp('Example_Corp')
    print(device1.__dict__)

    acp1 = AccessControlPolicy(fmc=fmc1)
    acp1.get(name='Example_Corp')
    print(acp1.__dict__)

    sz1 = SecurityZone(fmc=fmc1)
    sz1.post(name='Demo')
    sz1.get()
    sz1.delete()
    print(sz1.__dict__)

    port1 = ProtocolPort(fmc=fmc1, name='_porter', port='8888', protocol='tcp')
    port1.post()
    port1.port='9999'
    port1.put()
    print(port1.__dict__)
    port1.delete()
    print(port1.__dict__)

    host2 = HostObject(fmc=fmc1)
    stuff =host2.get()
    print(stuff)

    host1 = HostObject(fmc=fmc1, name='daxm', value='1.2.3.4')
    host1.post()
    host1.value = '2.7.7.7'
    host1.get()
    print(host1.__dict__)

    host3 = HostObject(fmc=fmc1)
    host3.name = 'daxm'
    host3.get()
    host3.delete()
    print(host3.__dict__)

    url1 = URL(fmc=fmc1, name='daxm.net', url='daxm.net')
    url1.post()
    url1.url='www.daxm.net'
    url1.put()
    print(url1.__dict__)
    url1.delete()
    print(url1.__dict__)
'''
