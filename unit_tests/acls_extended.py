import logging
import fmcapi
import time

def test__extended_acls(fmc):
    logging.info("Testing ExtendedAccessList class.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    ext_acl = fmcapi.ExtendedAccessList(fmc=fmc)
    ext_acl.name = namer
    ext_acl.entries = []

    ace = fmcapi.ExtendedAccessListAce()
    ace.action = "DENY"
    ace.destinationNetworksLiterals = [
        {
            "type" : "Host",
            "value": "1.1.1.1"
        }
    ]

    ext_acl.entries.append(ace.build_ace())
    ext_acl.post()
    logging.debug(ext_acl.get())

    ace.destinationNetworksLiterals = [
        {
            "type" : "Host",
            "value": "2.2.2.2"
        }
    ]

    ext_acl.entries.append(ace.build_ace())
    logging.debug(ext_acl.entries)
    ext_acl.put()
    logging.debug(ext_acl.get())
    ext_acl.delete()
    del ext_acl
    logging.info("Testing ExtendedAccessList class done.\n")
