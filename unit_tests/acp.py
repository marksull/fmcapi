import logging
import fmcapi
import time


def test__access_control_policy(fmc):
    logging.info("Test AccessControlPolicy.  Post, get, put, delete ACP Objects.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    obj1 = fmcapi.AccessPolicies(fmc=fmc)
    obj1.name = namer
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = fmcapi.AccessPolicies(fmc=fmc, name=namer)
    obj1.get()
    obj1.name = "asdfasdf"
    obj1.put()
    time.sleep(1)
    obj1.delete()
    logging.info("Test AccessControlPolicy done.\n")
