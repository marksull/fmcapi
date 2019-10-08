import logging
import fmcapi
import time
from unit_tests import wait_for_task


def test__device_with_task(fmc):
    logging.info(
        'Test Device1 with Task.  This requires having an actual device with the "configure manager add" '
        "statement enabled."
    )

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    acp1 = fmcapi.AccessPolicies(fmc=fmc, name=namer)
    acp1.post()

    starttime = str(int(time.time()))
    obj1_namer = f"_fmcapi_test_{starttime}"

    obj1 = fmcapi.Device(fmc=fmc)
    obj1.hostName = "10.255.0.43"
    obj1.name = obj1_namer
    obj1.regKey = "cisco123"
    obj1.natID = "cisco123"
    obj1.acp(name=acp1.name)
    obj1.licensing(action="add", name="BASE")
    obj1.licensing(action="add", name="THREAT")
    obj1.licensing(action="add", name="MALWARE")
    logging.info("Device -->")
    logging.info(obj1.format_data())

    response = obj1.post()
    wait_for_task(response["metadata"]["task"], 30)
    logging.info(
        'Test Device2 with Task.  This requires having an actual device with the "configure manager add" '
        "statement enabled."
    )

    starttime = str(int(time.time()))
    obj2_namer = f"_fmcapi_test_{starttime}"

    obj2 = fmcapi.Device(fmc=fmc)
    obj2.hostName = "10.255.0.44"
    obj2.name = obj2_namer
    obj2.regKey = "cisco123"
    obj2.natID = "cisco123"
    obj2.acp(name=acp1.name)
    obj2.licensing(action="add", name="BASE")
    obj2.licensing(action="add", name="THREAT")
    obj2.licensing(action="add", name="MALWARE")
    logging.info("Device -->")
    logging.info(obj2.format_data())
    logging.info("\n")
    obj2.post()
    # wait_for_task(response["metadata"]["task"], 30)

    # Wait some additional time to complete device registration before deletion
    time.sleep(180)
    obj1 = fmcapi.Device(fmc=fmc)
    obj2 = fmcapi.Device(fmc=fmc)
    obj1.get(name=obj1_namer)
    obj2.get(name=obj2_namer)

    obj1.delete()
    time.sleep(30)
    obj2.delete()
    time.sleep(30)
    acp1.delete()
