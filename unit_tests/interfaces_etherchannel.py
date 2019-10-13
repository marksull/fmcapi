import logging
import fmcapi
import time


def test__etherchannel_interfaces(fmc):
    logging.info(
        "Test EtherchannelInterfaces.  get, post, put, delete EtherchannelInterfaces Objects. "
        "Requires registered physical device"
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

    eth1 = fmcapi.EtherchannelInterfaces(fmc=fmc, device_name="device_name")
    eth1.p_interfaces(
        p_interfaces=["GigabitEthernet0/3", "GigabitEthernet0/5"],
        device_name="device_name",
    )
    eth1.enabled = True
    eth1.ifname = "_eth1" + namer
    eth1.etherChannelId = "1"
    eth1.static(ipv4addr="192.0.2.1", ipv4mask=24)
    eth1.sz(name=sz1.name)
    eth1.mode = "NONE"
    eth1.MTU = "1500"
    eth1.lacpMode = "ACTIVE"
    eth1.loadBalancing = "SRC_DST_IP_PORT"
    eth1.post()
    time.sleep(2)

    eth1.get()
    eth1.enabled = False
    eth1.sz(name=sz2.name)
    eth1.put()
    time.sleep(1)

    eth1.get()
    eth1.delete()
    sz1.delete()
    sz2.delete()

    logging.info("Testing EtherchannelInterfaces class done.\n")
