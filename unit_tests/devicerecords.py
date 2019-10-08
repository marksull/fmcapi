import logging
import fmcapi
import time


def test__devicerecords(fmc):
    logging.info(
        'Test Device.  Though you can "Post" devices I do not have one handy. So '
        "add/remove licenses on Device Objects."
    )

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    acp1 = fmcapi.AccessPolicies(fmc=fmc, name=namer)
    acp1.post()
    obj1 = fmcapi.DeviceRecords(fmc=fmc)
    obj1.name = namer
    obj1.acp(name=acp1.name)
    obj1.licensing(action="add", name="MALWARE")
    obj1.licensing(action="add", name="VPN")
    obj1.licensing(action="remove", name="VPN")
    obj1.licensing(action="clear")
    obj1.licensing(action="add", name="BASE")
    logging.info("Device -->")
    logging.info(obj1.format_data())

    acp1.delete()

    logging.info("Test Device done.\n")
