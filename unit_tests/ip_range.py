import logging
import fmcapi
import time
from .helper_functions import id_generator


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

    obj = fmcapi.Ranges(fmc=fmc)
    obj.bulk = []
    for i in range(13):
        obj.bulk.append(
            {
                "name" : f"_fmcapi_test_{id_generator()}",
                "value" : "3.3.3.3-4.4.4.4"
            }
        )
    obj.bulk_post()
    obj.bulk = obj.bulk_ids
    obj.bulk_delete()
    del obj

    obj = fmcapi.Ranges(fmc=fmc)
    obj.bulk = []
    for i in range(50):
        obj.bulk.append(
            {
                "name" : f"_fmcapi_test_{id_generator()}",
                "value" : "3.3.3.3-4.4.4.4"
            }
        )
    obj.bulk_post()
    obj.bulk = obj.bulk_ids
    obj.bulk_delete()
    del obj

    logging.info("Test IPRange done.\n")
