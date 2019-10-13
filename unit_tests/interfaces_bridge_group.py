import logging
import fmcapi
import time


def test__bridge_group_interfaces(fmc):
    logging.info(
        "Test BridgeGroupInterfaces.  get, post, put, delete BridgeGroupInterfaces Objects. "
        "Requires registered device"
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

    br1 = fmcapi.BridgeGroupInterfaces(fmc=fmc, device_name="device_name")
    br1.p_interfaces(
        p_interfaces=["GigabitEthernet0/3", "GigabitEthernet0/5"],
        device_name="device_name",
    )
    br1.enabled = True
    br1.ifname = "_br1" + namer
    br1.bridgeGroupId = "1"
    br1.static(ipv4addr="192.0.2.1", ipv4mask=24)
    br1.sz(name=sz1.name)
    br1.post()
    time.sleep(2)

    br1.get()
    br1.enabled = False
    br1.sz(name=sz2.name)
    br1.put()
    time.sleep(1)

    br1.get()
    br1.delete()
    sz1.delete()
    sz2.delete()

    logging.info("Testing BridgeGroupInterfaces class done.\n")
