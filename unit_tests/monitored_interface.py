import logging
import fmcapi


def test__monitoredinterfaces(fmc):
    logging.info("Test MonitoredInterfaces. get, put MonitoredInterfaces Objects")

    obj0 = fmcapi.DeviceHAMonitoredInterfaces(fmc=fmc, ha_name="HaName")
    obj1 = fmcapi.MonitoredInterfaces(fmc=fmc, ha_name="HaName")
    # Interface logical name (ifname)
    obj1.get(name="OUTSIDE1")
    obj1.monitorForFailures = True
    obj1.ipv4(ipv4addr="10.254.0.4", ipv4mask=29, ipv4standbyaddr="10.254.0.3")
    logging.info("MonitoredInterfaces PUT-->")
    logging.info(obj1.format_data())

    logging.info(obj1.put())
