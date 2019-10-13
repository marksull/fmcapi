import logging
import fmcapi
import time


def test__ftddevicehapairs(fmc):
    logging.info(
        'Test FTDDeviceHAPairs. After an HA Pair is created, all API calls to "devicerecords" objects should '
        "be directed at the currently active device not the ha pair"
    )
    failover1 = fmcapi.PhysicalInterfaces(fmc=fmc)
    failover1.get(device_name="PrimaryName", name="GigabitEthernet0/6")
    stateful1 = fmcapi.PhysicalInterfaces(fmc=fmc)
    stateful1.get(device_name="PrimaryName", name="GigabitEthernet0/7")
    obj0 = fmcapi.DeviceHAPairs(fmc=fmc)
    obj1 = fmcapi.FTDDeviceHAPairs(fmc=fmc)
    obj1.primary(name="PrimaryName")
    obj1.secondary(name="SecondaryName")
    obj1.name = "HaName"
    # failover interface subnetMask must be in x.x.x.x format"
    obj1.ftdHABootstrap = {
        "isEncryptionEnabled": "true",
        "encKeyGenerationScheme": "CUSTOM",
        "sharedKey": "cisco123",
        "useSameLinkForFailovers": False,
        "lanFailover": {
            "useIPv6Address": False,
            "subnetMask": "255.255.255.252",
            "interfaceObject": {
                "type": "PhysicalInterface",
                "name": failover1.name,
                "id": failover1.id,
            },
            "standbyIP": "192.168.1.2",
            "logicalName": "HA-FAILOVER",
            "activeIP": "192.168.1.1",
        },
        "statefulFailover": {
            "useIPv6Address": False,
            "subnetMask": "255.255.255.252",
            "interfaceObject": {
                "type": "PhysicalInterface",
                "name": stateful1.name,
                "id": stateful1.id,
            },
            "standbyIP": "192.168.1.6",
            "logicalName": "HA-STATEFUL",
            "activeIP": "192.168.1.5",
        },
    }
    # response = ha_pair.post()
    # wait_for_task(response["metadata"]["task"], 30)
    logging.info("Device HA-->")
    logging.info(obj1.format_data())
    logging.info("\n")
    obj1.post()
    time.sleep(300)
    del obj1

    obj1 = fmcapi.FTDDeviceHAPairs(fmc=fmc, name="HaName")
    obj1.switch_ha()
    logging.info("Device HA Switch-->")
    logging.info(obj1.format_data())
    logging.info("\n")
    response = obj1.put()
    logging.info(response)
    time.sleep(20)
    del obj1

    obj1 = fmcapi.FTDDeviceHAPairs(fmc=fmc, name="HaName")
    obj1.break_ha()
    logging.info("Device HA Break-->")
    logging.info(obj1.format_data())
    logging.info("\n")
    response = obj1.put()
    logging.info(response)

    time.sleep(300)
    del obj1
    obj1 = fmcapi.FTDDeviceHAPairs(fmc=fmc)
    obj1.get(name="FTDv-HA2")

    #  Deleting the HAPair object will delete the HA configuration AND remove the devices from the FMC
    obj1.delete()
