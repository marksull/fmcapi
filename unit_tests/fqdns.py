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
    for i in range(50):
        obj.bulk.append(
            {
                "name" : f"_fmcapi_test_{id_generator()}",
                "value" : "www.cisco.com",
                "dnsResolution" : "IPV4_ONLY"
            }
        )
    obj.bulk_post()

    # sleep a bit otherwise the api just doesn't know that these objects are unused immediately after post
    time.sleep(10)

    ids = []
    fqdn_obs = fmcapi.FQDNS(fmc=fmc)
    # getting unused fqdn & ranges objects from fmc api is broken in 7.6
    unused_fqdn = fqdn_obs.get(unusedOnly=True)
    if 'items' in unused_fqdn:
        for obj in unused_fqdn['items']:
            ids.append(obj['id'])

        bulk_delete = fmcapi.FQDNS(fmc=fmc)
        bulk_delete.bulk = ids
        bulk_delete.bulk_delete()
    else:
        logging.info(f'No unused objects to bulk delete')

    logging.info("FQDNS DNSServerGroups class done.\n")
