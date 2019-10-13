import logging
import fmcapi
import time


def test__redundant_interfaces(fmc):
    logging.info(
        "Test RedundantInterfaces.  get, post, put, delete RedundantInterfaces Objects. Requires registered device"
    )

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    sz1 = fmcapi.SecurityZones(fmc=fmc)
    sz1.name = "_sz1" + namer
    sz1.post()
    time.sleep(1)
    sz2 = fmcapi.SecurityZones(fmc=fmc)
    sz2.name = "_sz2" + namer
    sz2.post()
    time.sleep(1)

    red1 = fmcapi.RedundantInterfaces(fmc=fmc, device_name="device_name")
    red1.primary(p_interface="GigabitEthernet0/3", device_name="device_name")
    red1.secondary(p_interface="GigabitEthernet0/5", device_name="device_name")
    red1.enabled = "True"
    red1.ifname = "_red1" + namer
    red1.redundantId = "1"
    red1.static(ipv4addr="192.0.2.1", ipv4mask=24)
    red1.sz(name=sz1.name)
    red1.post()
    time.sleep(2)

    red1.get()
    logging.info(red1.format_data())
    red1.enabled = False
    red1.sz(name=sz2.name)
    red1.put()
    time.sleep(1)

    red1.get()
    logging.info(red1.format_data())
    red1.delete()
    sz1.delete()
    sz2.delete()

    logging.info("Testing RedundantInterfaces class done.\n")
