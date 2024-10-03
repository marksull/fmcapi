import logging
import fmcapi
import time
from .helper_functions import id_generator

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

    obj = fmcapi.Networks(fmc=fmc)
    obj.bulk = []
    for i in range(15):
        obj.bulk.append(
            {
                "name" : f"_fmcapi_test_{id_generator()}",
                "value" : "9.9.9.0/24"
            }
        )
    obj.bulk_post()
    obj.bulk = obj.bulk_ids
    obj.bulk_delete()
    del obj

    obj = fmcapi.Networks(fmc=fmc)
    obj.bulk = []
    for i in range(50):
        obj.bulk.append(
            {
                "name" : f"_fmcapi_test_{id_generator()}",
                "value" : "9.9.9.0/24"
            }
        )
    obj.bulk_post()
    obj.bulk = obj.bulk_ids
    obj.bulk_delete()
    del obj

    logging.info("Test IPNetwork done.\n")
