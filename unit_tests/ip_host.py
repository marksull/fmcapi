import logging
import fmcapi
import time
from .helper_functions import id_generator

def test__ip_host(fmc):
    logging.info("Test IPHost.  Post, get, put, delete Host Objects.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    obj1 = fmcapi.Hosts(fmc=fmc)
    obj1.name = namer
    obj1.value = "8.8.8.8/32"
    obj1.post()
    time.sleep(1)
    del obj1

    obj1 = fmcapi.Hosts(fmc=fmc, name=namer)
    obj1.get()
    obj1.value = "9.9.9.9"
    obj1.put()
    time.sleep(1)
    obj1.delete()
    del obj1

    obj = fmcapi.Hosts(fmc=fmc)
    obj.bulk = []
    for i in range(5):
        obj.bulk.append(
            {
                "name" : f"_fmcapi_test_{id_generator()}",
                "value" : "9.9.9.9"
            }
        )
    obj.bulk_post()
    obj.bulk = obj.bulk_ids
    obj.bulk_delete()
    del obj

    obj = fmcapi.Hosts(fmc=fmc)
    obj.bulk = []
    for i in range(50):
        obj.bulk.append(
            {
                "name" : f"_fmcapi_test_{id_generator()}",
                "value" : "9.9.9.9"
            }
        )
    obj.bulk_post()
    obj.bulk = obj.bulk_ids
    obj.bulk_delete()
    del obj

    logging.info("Test IPHost done.\n")
