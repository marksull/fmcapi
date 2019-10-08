import logging
import fmcapi
import time


def test__ipv6staticroutes(fmc):
    logging.info(
        "Testing IPv6StaticRoutes class. get, post, put, delete IPv4StaticRoute Objects. Requires a registered device"
    )

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    iphost1 = fmcapi.Hosts(fmc=fmc, name="_iphost1" + namer, value="2001:db8::1")
    iphost1.post()
    ipnet1 = fmcapi.Networks(fmc=fmc, name="_ipnet1" + namer, value="2001:db8:1::/64")
    ipnet2 = fmcapi.Networks(fmc=fmc, name="_ipnet2" + namer, value="2001:db8:2::/64")
    ipnet1.post()
    ipnet2.post()

    ipv4route1 = fmcapi.IPv6StaticRoutes(fmc=fmc, name="_ipv6route1")
    ipv4route1.device(device_name="ftdv01.ccie.lab")
    ipv4route1.networks(action="add", networks=[ipnet1.name, ipnet2.name])
    ipv4route1.gw(name=iphost1.name)
    ipv4route1.interfaceName = "ifname"
    ipv4route1.metricValue = 1
    result = ipv4route1.post()

    ipv4route2 = fmcapi.IPv4StaticRoutes(fmc=fmc, name="_ipv6route1")
    ipv4route2.device(device_name="device_name")
    ipv4route2.id = result["id"]
    ipv4route2.get()

    del ipv4route1
    ipv4route2.networks(action="remove", networks=[ipnet2.name])
    ipv4route2.put()

    ipv4route2.delete()
    ipnet1.delete()
    ipnet2.delete()
    iphost1.delete()
    logging.info("Testing IPv6StaticRoutes class done.\n")
