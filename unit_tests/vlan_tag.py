import logging
import fmcapi
import time


def test__vlan_tag(fmc):
    logging.info("Test VlanTag.  Post, get, put, delete VLAN Tag Objects.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    obj1 = fmcapi.VlanTags(fmc=fmc)
    obj1.name = namer
    obj1.vlans(start_vlan="100", end_vlan="200")
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = fmcapi.VlanTags(fmc=fmc, name=namer)
    obj1.get()
    obj1.vlans(start_vlan="400", end_vlan="300")
    obj1.put()
    time.sleep(1)
    obj1.delete()

    logging.info("Test VlanTag done.\n")
