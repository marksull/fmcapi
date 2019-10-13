import logging
import fmcapi
import time


def test__interface_group(fmc):
    logging.info("Test InterfaceGroup.  Post, get, put, delete InterfaceGroup Objects.")

    obj1 = fmcapi.InterfaceGroups(fmc=fmc)
    obj1.name = "_ig_outside_all"
    obj1.interfaceMode = "ROUTED"
    logging.info("InterfaceGroup POST-->")
    logging.info(obj1.format_data())
    logging.info("\n")
    obj1.post()
    time.sleep(1)
    del obj1

    obj1 = fmcapi.InterfaceGroups(fmc=fmc, name="_ig_outside_all")
    obj1.get()
    obj1.p_interface(
        device_name="device_name",
        action="add",
        names=["GigabitEthernet0/0", "GigabitEthernet0/1", "GigabitEthernet0/2"],
    )
    logging.info("InterfaceGroup PUT-->")
    logging.info(obj1.format_data())
    logging.info("\n")
    obj1.put()
    time.sleep(1)
    del obj1

    obj1 = fmcapi.InterfaceGroups(fmc=fmc, name="_ig_outside_all")
    obj1.get()
    obj1.p_interface(
        device_name="device_name", action="remove", names=["GigabitEthernet0/1"]
    )
    logging.info("InterfaceGroup PUT-->")
    logging.info(obj1.format_data())
    logging.info("\n")
    obj1.put()
    time.sleep(1)
    del obj1

    obj1 = fmcapi.InterfaceGroups(fmc=fmc, name="_ig_outside_all")
    obj1.get()
    obj1.p_interface(action="clear-all")
    obj1.put()
    logging.info("InterfaceGroup DELETE-->")
    logging.info(obj1.format_data())
    logging.info("\n")
    obj1.delete()
    del obj1

    logging.info("Test InterfaceGroup done.\n")
