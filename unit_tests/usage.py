import logging
import fmcapi
import time
import json


def test__usage(fmc):
    logging.info("Test Object Find Usage.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    obj1 = fmcapi.Hosts(fmc=fmc)
    obj1.name = namer
    obj1.value = "8.8.8.8/32"
    obj1.post()
    time.sleep(1)
    obj2 = fmcapi.Usage(fmc=fmc)
    obj2.get(uuid=obj1.id, type=obj1.type)
    time.sleep(1)
    obj1.delete()
    del obj1
    del obj2

    logging.info("Test Object Find Usage done.\n")