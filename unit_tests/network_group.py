import logging
import fmcapi
import time


def test__network_group(fmc):
    logging.info("Testing NetworkGroup class.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    obj10 = fmcapi.Hosts(fmc=fmc, name="_iphost1", value="3.3.3.3")
    obj10.post()
    obj11 = fmcapi.Networks(fmc=fmc, name="_ipnet1", value="3.3.3.0/24")
    obj11.post()
    obj12 = fmcapi.Ranges(fmc=fmc, name="_iprange1", value="3.3.3.3-33.33.33.33")
    obj12.post()
    time.sleep(1)

    obj1 = fmcapi.NetworkGroups(fmc=fmc, name=namer)
    obj1.named_networks(action="add", name=obj10.name)
    obj1.named_networks(action="add", name=obj10.name)
    obj1.named_networks(action="remove", name=obj10.name)
    obj1.named_networks(action="clear")
    obj1.named_networks(action="add", name=obj11.name)
    obj1.named_networks(action="add", name=obj12.name)
    obj1.named_networks(action="remove", name=obj11.name)
    obj1.post()
    time.sleep(1)
    del obj1

    obj1 = fmcapi.NetworkGroups(fmc=fmc, name=namer)
    obj1.get()
    obj1.unnamed_networks(action="add", value="1.2.3.4")
    obj1.unnamed_networks(action="clear")
    obj1.unnamed_networks(action="add", value="1.2.3.4")
    obj1.unnamed_networks(action="remove", value="1.2.3.4")
    obj1.unnamed_networks(action="add", value="6.7.8.9")
    obj1.unnamed_networks(action="add", value="1.2.3.0/24")
    obj1.post()

    time.sleep(1)
    obj1.delete()
    obj10.delete()
    obj11.delete()
    obj12.delete()

    logging.info("Testing NetworkGroup class done.\n")
