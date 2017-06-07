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
    host1 = HostObject(fmc=fmc1, name='daxm', value='1.2.3.4')
    host1.post()
    host1.value = '2.7.7.7'
    host1.put()
