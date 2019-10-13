import logging
import fmcapi
import time


def test__ip_network(fmc):
    logging.info("Test IPNetwork.  Post, get, put, delete Network Objects.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    obj1 = fmcapi.Networks(fmc=fmc)
    obj1.name = namer
    obj1.value = "8.8.8.0/24"
    obj1.post()
    time.sleep(1)
    del obj1

    obj1 = fmcapi.Networks(fmc=fmc, name=namer)
    obj1.get()
    obj1.value = "9.9.9.0/24"
    obj1.put()
    time.sleep(1)
    obj1.delete()

    logging.info("Test IPNetwork done.\n")
