import logging
import fmcapi
import time
from .helper_functions import id_generator


def test__fqdns(fmc):
    logging.info("Test FQDNS.  Post, get, put, delete FQDNS Objects.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    obj1 = fmcapi.FQDNS(fmc=fmc)
    obj1.name = "_fqdns1" + namer
    obj1.value = "www.cisco.com"
    obj1.dnsResolution = "IPV4_ONLY"
    obj1.post()

    obj1.get()
    obj1.dnsResolution = "IPV4_AND_IPV6"
    obj1.put()

    obj1.delete()

    obj = fmcapi.FQDNS(fmc=fmc)
    obj.bulk = []
    for i in range(10):
        obj.bulk.append(
            {
                "name" : f"_fmcapi_test_{id_generator()}",
                "value" : "www.cisco.com",
                "dnsResolution" : "IPV4_ONLY"
            }
        )
    obj.bulk_post()
    obj.bulk = obj.bulk_ids
    obj.bulk_delete()
    del obj

    obj = fmcapi.FQDNS(fmc=fmc)
    obj.bulk = []
    for i in range(50):
        obj.bulk.append(
            {
                "name" : f"_fmcapi_test_{id_generator()}",
                "value" : "www.cisco.com",
                "dnsResolution" : "IPV4_ONLY"
            }
        )
    obj.bulk_post()
    obj.bulk = obj.bulk_ids
    obj.bulk_delete()
    del obj

    logging.info("FQDNS DNSServerGroups class done.\n")
