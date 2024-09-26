import logging
import fmcapi
import time
from .helper_functions import id_generator


def test__protocol_port(fmc):
    logging.info("Test ProtocolPort.  Post, get, put, delete Port Objects.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    obj1 = fmcapi.ProtocolPortObjects(fmc=fmc)
    obj1.name = namer
    obj1.port = "1234"
    obj1.protocol = "TCP"
    obj1.post()
    time.sleep(1)
    del obj1

    obj1 = fmcapi.ProtocolPortObjects(fmc=fmc, name=namer)
    obj1.get()
    obj1.port = "5678"
    obj1.put()
    time.sleep(1)
    obj1.delete()


    obj = fmcapi.ProtocolPortObjects(fmc=fmc)
    obj.bulk = []
    for i in range(50):
        obj.bulk.append(
            {
                "name" : f"_fmcapi_test_{id_generator()}",
                "protocol" : "TCP",
                "port" : "5678"
            }
        )
    obj.bulk_post()

    # sleep a bit otherwise the api just doesn't know that these objects are unused immediately after post
    time.sleep(10)

    ids = []
    protocol_port_obs = fmcapi.ProtocolPortObjects(fmc=fmc)
    protocol_port_obs.expanded=True
    unused_protocol_ports = protocol_port_obs.get(unusedOnly=True)
    if 'items' in unused_protocol_ports:
        for obj in unused_protocol_ports['items']:
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

    logging.info("Test ProtocolPort done.\n")
