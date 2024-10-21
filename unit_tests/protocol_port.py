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
    for i in range(12):
        obj.bulk.append(
            {
                "name" : f"_fmcapi_test_{id_generator()}",
                "protocol" : "TCP",
                "port" : "5678"
            }
        )
    obj.bulk_post()
    obj.bulk = obj.bulk_ids
    obj.bulk_delete()
    del obj

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
    obj.bulk = obj.bulk_ids
    obj.bulk_delete()
    del obj

    logging.info("Test ProtocolPort done.\n")
