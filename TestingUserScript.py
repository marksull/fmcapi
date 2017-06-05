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
    logging.info("fmc1 instantiated.")
