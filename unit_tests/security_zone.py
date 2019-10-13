import logging
import fmcapi
import time


def test__security_zone(fmc):
    logging.info("Test SecurityZone.  Post, get, put, delete Security Zone Objects.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    obj1 = fmcapi.SecurityZones(fmc=fmc)
    obj1.name = namer
    obj1.interfaceMode = "ROUTED"
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = fmcapi.SecurityZones(fmc=fmc, name=namer)
    obj1.get()
    obj1.name = "DEMO"
    obj1.put()
    time.sleep(1)
    obj1.delete()
    logging.info("Test SecurityZone done.\n")
