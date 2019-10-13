import logging
import fmcapi
import time


def test__devicegrouprecords(fmc):
    logging.info(
        "Test DeviceGroupRecords: "
        "get, post, put, delete DeviceGroupRecords Objects requires registered device"
    )

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    device_list = [{"name": "ftdv-HA", "type": "deviceHAPair"}]
    dg1 = fmcapi.DeviceGroupRecords(fmc=fmc)
    dg1.name = "_dg1" + namer
    dg1.devices(action="add", members=device_list)
    dg1.post()
    time.sleep(1)

    dg1.get()
    dg1.devices(action="remove", members=device_list)
    dg1.put()
    time.sleep(1)

    dg1.get()
    dg1.devices(action="add", members=device_list)
    dg1.put()
    time.sleep(1)

    dg1.get()
    dg1.devices(action="clear")
    dg1.put()
    time.sleep(1)

    dg1.get()
    dg1.delete()
    logging.info("Testing DeviceGroupRecords class done.\n")
