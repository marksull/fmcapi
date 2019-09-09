import logging
import fmcapi
import time


def test__device_group(fmc):
    logging.info('Test DeviceGroups.  get, post, put, delete DeviceGroups Objects. Requires registered device')

    starttime = str(int(time.time()))
    namer = f'_fmcapi_test_{starttime}'

    device_list = [{"name": "ftdv-HA", "type": "deviceHAPair"}]
    dg1 = fmcapi.DeviceGroups(fmc=fmc)
    dg1.name = "_dg1" + namer
    dg1.devices(action='add', members=device_list)
    dg1.post()
    time.sleep(1)

    dg1.get()
    dg1.devices(action='remove', members=device_list)
    dg1.put()
    time.sleep(1)

    dg1.get()
    dg1.devices(action='add', members=device_list)
    dg1.put()
    time.sleep(1)

    dg1.get()
    dg1.devices(action='clear')
    dg1.put()
    time.sleep(1)

    dg1.get()
    dg1.delete()
    logging.info('Testing DeviceGroups class done.\n')
