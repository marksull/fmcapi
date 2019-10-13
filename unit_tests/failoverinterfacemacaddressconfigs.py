import logging
import fmcapi


def test__failoverinterfacemacaddressconfigs(fmc):
    logging.info(
        "Test FailoverInterfaceMACAddressConfigs. get, post, put, "
        "delete FailoverInterfaceMACAddressConfigs Objects"
    )

    obj1 = fmcapi.DeviceHAFailoverMAC(fmc=fmc, ha_name="HaName")
    obj1.p_interface(name="GigabitEthernet0/0", device_name="device_name")
    obj1.failoverActiveMac = "0050.5686.718f"
    obj1.failoverStandbyMac = "1050.5686.0c2e"
    logging.info("DeviceHAFailoverMAC POST->")
    logging.info(obj1.format_data())

    obj1.post()
    del obj1

    obj1 = fmcapi.DeviceHAFailoverMAC(fmc=fmc)
    obj1.edit(name="GigabitEthernet0/0", ha_name="HaName")
    obj1.failoverStandbyMac = "0050.5686.0c2e"
    logging.info("DeviceHAFailoverMAC PUT->")

    logging.info(obj1.format_data())
    del obj1

    obj1 = fmcapi.DeviceHAFailoverMAC(fmc=fmc)
    obj1.edit(name="GigabitEthernet0/0", ha_name="HaName")
    obj1.delete()
