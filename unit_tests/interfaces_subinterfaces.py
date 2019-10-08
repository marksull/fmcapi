import logging
import fmcapi
import time


def test__subinterfaces(fmc):
    logging.info(
        "Test SubInterfaces.  get, post, put, delete SubInterfaces Objects. Requires registered device"
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

    sub1 = fmcapi.SubInterfaces(fmc=fmc, device_name="device_name")
    sub1.p_interface(p_interface="GigabitEthernet0/3", device_name="device_name")
    sub1.enabled = True
    sub1.ifname = "_sub1" + namer
    sub1.subIntfId = "300"
    sub1.vlanId = "300"
    sub1.static(ipv4addr="192.0.2.1", ipv4mask=24)
    sub1.sz(name=sz1.name)
    sub1.post()
    logging.info(sub1.format_data())
    time.sleep(2)

    sub1.get()
    sub1.enabled = False
    sub1.sz(name=sz2.name)
    sub1.put()
    time.sleep(1)

    sub1.get()
    sub1.delete()
    sz1.delete()
    sz2.delete()

    logging.info("Testing SubInterfaces class done.\n")
