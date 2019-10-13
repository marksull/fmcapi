import logging
import fmcapi
import time


def test__ip_range(fmc):
    logging.info("Test IPRange.  Post, get, put, delete Range Objects.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    obj1 = fmcapi.Ranges(fmc=fmc)
    obj1.name = namer
    obj1.value = "1.1.1.1-2.2.2.2"
    obj1.post()
    time.sleep(1)
    del obj1

    obj1 = fmcapi.Ranges(fmc=fmc, name=namer)
    obj1.get()
    obj1.value = "3.3.3.3-4.4.4.4"
    obj1.put()
    time.sleep(1)
    obj1.delete()

    logging.info("Test IPRange done.\n")
