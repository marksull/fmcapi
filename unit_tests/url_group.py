import logging
import fmcapi
import time


def test__url_group(fmc):
    logging.info("Testing URLGroup class.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    url1 = fmcapi.URLs(fmc=fmc, name="_url1", url="example.org")
    url1.post()
    url2 = fmcapi.URLs(fmc=fmc, name="_url2", url="example.net")
    url2.post()
    url3 = fmcapi.URLs(fmc=fmc, name="_url3", url="example.com")
    url3.post()
    time.sleep(1)
    obj1 = fmcapi.URLGroups(fmc=fmc, name=namer)
    obj1.named_urls(action="add", name=url1.name)
    obj1.named_urls(action="add", name=url1.name)
    obj1.named_urls(action="clear")
    obj1.named_urls(action="add", name=url2.name)
    obj1.named_urls(action="add", name=url3.name)
    obj1.named_urls(action="add", name=url1.name)
    obj1.named_urls(action="remove", name=url3.name)
    obj1.post()
    time.sleep(1)
    del obj1
    obj1 = fmcapi.URLGroups(fmc=fmc, name=namer)
    obj1.get()
    obj1.unnamed_urls(action="add", value="daxm.net")
    obj1.unnamed_urls(action="add", value="daxm.com")
    obj1.unnamed_urls(action="clear")
    obj1.unnamed_urls(action="add", value="daxm.org")
    obj1.unnamed_urls(action="add", value="daxm.net")
    obj1.unnamed_urls(action="add", value="daxm.lan")
    obj1.unnamed_urls(action="remove", value="daxm.org")
    obj1.put()
    time.sleep(1)
    obj1.delete()
    url1.delete()
    url2.delete()
    url3.delete()

    logging.info("Testing URLGroup class done.\n")
