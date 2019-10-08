import logging
import fmcapi
import time


def test__port_object_group(fmc):
    logging.info("Testing PortObjectGroup class.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    obj10 = fmcapi.ProtocolPortObjects(
        fmc=fmc, name="_porttcp1", port="8443", protocol="TCP"
    )
    obj10.post()
    obj11 = fmcapi.ProtocolPortObjects(
        fmc=fmc, name="_portudp1", port="161", protocol="UDP"
    )
    obj11.post()
    obj12 = fmcapi.ProtocolPortObjects(
        fmc=fmc, name="_portrangetcp1", port="0-1023", protocol="TCP"
    )
    obj12.post()
    time.sleep(1)
    obj1 = fmcapi.PortObjectGroups(fmc=fmc, name=namer)
    obj1.named_ports(action="add", name=obj10.name)
    obj1.named_ports(action="add", name=obj10.name)
    obj1.named_ports(action="remove", name=obj10.name)
    obj1.named_ports(action="clear")
    obj1.named_ports(action="add", name=obj11.name)
    obj1.named_ports(action="add", name=obj12.name)
    obj1.named_ports(action="remove", name=obj11.name)
    obj1.post()
    time.sleep(1)
    del obj1

    obj1 = fmcapi.PortObjectGroups(fmc=fmc, name=namer)
    obj1.get()
    obj1.named_ports(action="add", name="HTTP")
    obj1.named_ports(action="clear")
    obj1.named_ports(action="add", name="HTTP")
    obj1.named_ports(action="remove", name="HTTP")
    obj1.named_ports(action="add", name="HTTP")
    obj1.named_ports(action="add", name="HTTPS")
    obj1.put()

    time.sleep(1)
    obj1.delete()
    obj10.delete()
    obj11.delete()
    obj12.delete()

    logging.info("Testing PortObjectGroup class done.\n")
