import logging
import fmcapi
import time


def test__vlan_group_tag(fmc):
    logging.info("Testing VlanGroupTag class.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    obj10 = fmcapi.VlanTags(
        fmc=fmc, name="_vlantag10", data={"startTag": "888", "endTag": "999"}
    )
    obj10.post()
    obj11 = fmcapi.VlanTags(
        fmc=fmc, name="_vlantag11", data={"startTag": "222", "endTag": "333"}
    )
    obj11.post()
    obj12 = fmcapi.VlanTags(
        fmc=fmc, name="_vlantag12", data={"startTag": "1", "endTag": "999"}
    )
    obj12.post()
    time.sleep(1)
    obj1 = fmcapi.VlanGroupTags(fmc=fmc, name=namer)
    obj1.named_vlantags(action="add", name=obj10.name)
    obj1.named_vlantags(action="add", name=obj11.name)
    obj1.named_vlantags(action="remove", name=obj11.name)
    obj1.named_vlantags(action="clear")
    obj1.named_vlantags(action="add", name=obj10.name)
    obj1.named_vlantags(action="add", name=obj11.name)
    obj1.named_vlantags(action="add", name=obj12.name)
    obj1.named_vlantags(action="remove", name=obj12.name)
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = fmcapi.VlanGroupTags(fmc=fmc, name=namer)
    obj1.get()
    obj1.unnamed_vlantags(action="add", startvlan="22", endvlan="33")
    obj1.unnamed_vlantags(action="clear")
    obj1.unnamed_vlantags(action="add", startvlan="22", endvlan="33")
    obj1.unnamed_vlantags(action="remove", startvlan="22", endvlan="33")
    obj1.unnamed_vlantags(action="add", startvlan="44", endvlan="33")
    obj1.unnamed_vlantags(action="add", startvlan="900")
    obj1.put()
    time.sleep(1)
    obj1.delete()
    obj10.delete()
    obj11.delete()
    obj12.delete()

    logging.info("Testing VlanGroupTag class done.\n")
