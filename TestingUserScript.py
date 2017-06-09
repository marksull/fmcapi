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
    device1 = DeviceObject(fmc=fmc1)
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



'''
    acp1 = ACPPolicy(fmc=fmc1)
    acp1.get(name='Example_Corp')
    print(acp1.__dict__)

    sz1 = SecurityZoneObject(fmc=fmc1)
    sz1.post(name='Demo')
    sz1.get()
    sz1.delete()
    print(sz1.__dict__)

    port1 = PortObject(fmc=fmc1, name='_porter', port='8888', protocol='tcp')
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

    url1 = URLObject(fmc=fmc1, name='daxm.net', url='daxm.net')
    url1.post()
    url1.url='www.daxm.net'
    url1.put()
    print(url1.__dict__)
    url1.delete()
    print(url1.__dict__)
'''
