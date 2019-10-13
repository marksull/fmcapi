import logging
import fmcapi
import time


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
    logging.info("Test ProtocolPort done.\n")
