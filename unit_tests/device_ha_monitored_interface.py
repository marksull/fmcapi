import logging
import fmcapi
import pprint
pp = pprint.PrettyPrinter(indent=4)


def test__device_ha_monitored_interfaces(fmc):
    logging.info('Test DeviceHAMonitoredInterfaces. get, put DeviceHAMonitoredInterfaces Objects')

    obj1 = fmcapi.DeviceHAMonitoredInterfaces(fmc=fmc, ha_name="HaName")
    # Interface logical name (ifname)
    obj1.get(name="OUTSIDE1")
    obj1.monitorForFailures = True
    obj1.ipv4(ipv4addr="10.254.0.4", ipv4mask=29, ipv4standbyaddr="10.254.0.3")
    print('DeviceHAMonitoredInterfaces PUT-->')
    pp.pprint(obj1.format_data())
    print('\n')
    print(obj1.put())
