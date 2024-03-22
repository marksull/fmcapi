import logging
import fmcapi
import time
import json


def test__devicerecords(fmc):
    logging.info(
        'Test Device.  Though you can "Post" devices I do not have one handy. So '
        "add/remove licenses on Device Objects."
    )

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    all_device_records = fmcapi.DeviceRecords(fmc=fmc)
    all_device_records.get(expanded=True, includeOtherAssociatedPolicies=True)
    # Note: attached RAVPN policies output from 'includeOtherAssociatedPolicies=True'
    # have the INCORRECT UUID. Bug ID: CSCwj27112. This can be worked around for now
    # by subtracting 1 from the UUID in the response. This has ONLY been observed with
    # devicerecords api + 'includeOtherAssociatedPolicies=True' + ravpn policies.

    acp1 = fmcapi.AccessPolicies(fmc=fmc, name=namer)
    acp1.post()
    obj1 = fmcapi.DeviceRecords(fmc=fmc)
    obj1.name = namer
    obj1.acp(name=acp1.name)
    obj1.type = "Device"
    obj1.licensing(action="add", name="MALWARE")
    obj1.licensing(action="add", name="VPN")
    obj1.licensing(action="remove", name="VPN")
    obj1.licensing(action="clear")
    obj1.licensing(action="add", name="BASE")
    obj1.tiering(action="add", name="FTDv5")
    logging.info("Device -->")
    logging.info(obj1.format_data())

    acp1.delete()

    logging.info("Test Device done.\n")
