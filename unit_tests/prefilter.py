import logging
import fmcapi
import time


def test__prefilter_policy(fmc):
    logging.info("Test PreFilterPolicies.  Post, get, put, delete ACP Objects.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    obj1 = fmcapi.PreFilterPolicies(fmc=fmc)
    obj1.name = namer
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = fmcapi.PreFilterPolicies(fmc=fmc, name=namer)
    obj1.get()
    obj1.name = "asdfasdf"
    obj1.put()
    time.sleep(1)
    obj1.delete()
    logging.info("Test PreFilterPolicies done.\n")
