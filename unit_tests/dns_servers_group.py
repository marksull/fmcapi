import logging
import fmcapi
import time


def test__dns_servers_group(fmc):
    logging.info(
        "Test DNSServerGroups.  Post, get, put, delete DNSServerGroups Objects."
    )

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    server_list = ["192.0.2.1", "192.0.2.2"]
    obj1 = fmcapi.DNSServerGroups(fmc=fmc)
    obj1.name = "_dns1" + namer
    obj1.timeout = "3"
    obj1.defaultdomain = "cisco.com"
    obj1.post()

    obj1.get()
    obj1.servers(action="add", name_servers=server_list)
    obj1.put()

    obj1.delete()

    logging.info("Testing DNSServerGroups class done.\n")
