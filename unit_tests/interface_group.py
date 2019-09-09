import logging
import fmcapi
import time
import pprint
pp = pprint.PrettyPrinter(indent=4)


def test__interface_group(fmc):
    logging.info('Test InterfaceGroup.  Post, get, put, delete InterfaceGroup Objects.')

    obj1 = fmcapi.InterfaceGroup(fmc=fmc)
    obj1.name = "_ig_outside_all"
    obj1.interfaceMode = 'ROUTED'
    print('InterfaceGroup POST-->')
    pp.pprint(obj1.format_data())
    print('\n')
    obj1.post()
    time.sleep(1)
    del obj1

    obj1 = fmcapi.InterfaceGroup(fmc=fmc, name="_ig_outside_all")
    obj1.get()
    obj1.p_interface(device_name="device_name",
                     action="add",
                     names=["GigabitEthernet0/0", "GigabitEthernet0/1", "GigabitEthernet0/2"])
    print('InterfaceGroup PUT-->')
    pp.pprint(obj1.format_data())
    print('\n')
    obj1.put()
    time.sleep(1)
    del obj1

    obj1 = fmcapi.InterfaceGroup(fmc=fmc, name="_ig_outside_all")
    obj1.get()
    obj1.p_interface(device_name="device_name",
                     action="remove",
                     names=["GigabitEthernet0/1"])
    print('InterfaceGroup PUT-->')
    pp.pprint(obj1.format_data())
    print('\n')
    obj1.put()
    time.sleep(1)
    del obj1

    obj1 = fmcapi.InterfaceGroup(fmc=fmc, name="_ig_outside_all")
    obj1.get()
    obj1.p_interface(action="clear-all")
    obj1.put()
    print('InterfaceGroup DELETE-->')
    pp.pprint(obj1.format_data())
    print('\n')
    obj1.delete()
    del obj1
    logging.info('# Test InterfaceGroup done.\n')
