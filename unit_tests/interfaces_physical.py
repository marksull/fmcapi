import logging
import fmcapi
import time


def test__phys_interfaces(fmc):
    logging.info(
        "Test PhysicalInterface.  get, put PhysicalInterface Objects. Requires registered device"
    )

    sz1 = fmcapi.SecurityZones(fmc=fmc)
    sz1.name = "SZ-OUTSIDE1"
    sz1.post()
    time.sleep(1)
    sz2 = fmcapi.SecurityZones(fmc=fmc)
    sz2.name = "SZ-OUTSIDE2"
    sz2.post()
    time.sleep(1)

    intf1 = fmcapi.PhysicalInterfaces(fmc=fmc, device_name="device_name")
    intf1.get(name="GigabitEthernet0/0")
    intf1.enabled = True
    intf1.ifname = "OUTSIDE1"
    intf1.activeMACAddress = "0050.5686.718f"
    intf1.standbyMACAddress = "0050.5686.0c2e"
    intf1.static(ipv4addr="10.254.0.3", ipv4mask=24)
    intf1.sz(name=sz1.name)
    intf2 = fmcapi.PhysicalInterfaces(fmc=fmc, device_name="device_name")
    intf2.get(name="GigabitEthernet0/1")
    intf2.enabled = True
    intf2.ifname = "OUTSIDE2"
    intf2.activeMACAddress = "0050.5686.821d"
    intf2.standbyMACAddress = "0050.5686.11cb"
    intf2.dhcp()
    intf2.sz(name=sz2.name)
    intf1.put()
    time.sleep(1)
    intf2.put()
    time.sleep(1)
    intf1.get()
    intf2.get()

    intf1.enabled = False
    intf1.activeMACAddress = ""
    intf1.standbyMACAddress = ""
    intf1.static(ipv4addr="", ipv4mask="")
    intf1.securityZone = {}
    intf1.activeMACAddress = ""
    intf1.standbyMACAddress = ""
    intf2.enabled = False
    intf2.activeMACAddress = ""
    intf2.standbyMACAddress = ""
    intf2.static(ipv4addr="", ipv4mask="")
    intf2.securityZone = {}
    intf2.activeMACAddress = ""
    intf2.standbyMACAddress = ""
    intf1.put()
    time.sleep(1)
    intf2.put()
    time.sleep(1)
    intf1.get()
    intf2.get()
    intf1.ifname = ""
    intf2.ifname = ""
    intf1.put()
    sz1.delete()
    intf2.put()
    sz2.delete()
