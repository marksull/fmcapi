import logging
import fmcapi
import time


def test__url(fmc):
    logging.info("Test URL.  Post, get, put, delete URL Objects.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    obj1 = fmcapi.URLs(fmc=fmc)
    obj1.name = namer
    obj1.url = "daxm.com"
    obj1.post()
    time.sleep(1)
    del obj1

    obj1 = fmcapi.URLs(fmc=fmc, name=namer)
    obj1.get()
    obj1.url = "daxm.lan"
    obj1.put()
    time.sleep(1)
    obj1.delete()

    logging.info("Test URL done.\n")
