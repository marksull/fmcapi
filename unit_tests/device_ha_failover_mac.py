import logging
import fmcapi
import pprint
pp = pprint.PrettyPrinter(indent=4)


def test__device_ha_failover_mac(fmc):
    logging.info('Test DeviceHAFailoverMAC. get, post, put, delete DeviceHAFailoverMAC Objects')

    obj1 = fmcapi.DeviceHAFailoverMAC(fmc=fmc, ha_name="HaName")
    obj1.p_interface(name="GigabitEthernet0/0", device_name="device_name")
    obj1.failoverActiveMac = "0050.5686.718f"
    obj1.failoverStandbyMac = "1050.5686.0c2e"
    print('DeviceHAFailoverMAC POST->')
    pp.pprint(obj1.format_data())
    print('\n')
    obj1.post()
    del obj1

    obj1 = fmcapi.DeviceHAFailoverMAC(fmc=fmc)
    obj1.edit(name="GigabitEthernet0/0", ha_name="HaName")
    obj1.failoverStandbyMac = "0050.5686.0c2e"
    print('DeviceHAFailoverMAC PUT->')
    print('\n')
    pp.pprint(obj1.format_data())
    del obj1

    obj1 = fmcapi.DeviceHAFailoverMAC(fmc=fmc)
    obj1.edit(name="GigabitEthernet0/0", ha_name="HaName")
    obj1.delete()
