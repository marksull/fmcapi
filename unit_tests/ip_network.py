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
    for i in range(50):
        obj.bulk.append(
            {
                "name" : f"_fmcapi_test_{id_generator()}",
                "value" : "9.9.9.0/24"
            }
        )
    obj.bulk_post()

    # sleep a bit otherwise the api just doesn't know that these objects are unused immediately after post
    time.sleep(10)

    ids = []
    network_obs = fmcapi.Networks(fmc=fmc)
    network_obs.expanded=True
    unused_networks = network_obs.get(unusedOnly=True)
    if 'items' in unused_networks:
        for obj in unused_networks['items']:
            # Do not try and modify/delete system defined/readonly objects (ex. default RFC1918 object)
            if 'readOnly' not in obj['metadata']:
                ids.append(obj['id'])
            else:
                logging.info(f"{obj['id']} is a system defined read only object that happens to be unused. This will not be removed!")

        bulk_delete = fmcapi.Networks(fmc=fmc)
        bulk_delete.bulk = ids
        bulk_delete.bulk_delete()
    else:
        logging.info(f'No unused objects to bulk delete')

    logging.info("Test IPNetwork done.\n")
