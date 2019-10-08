import logging
import fmcapi
import time


def test__icmpv6(fmc):
    logging.info("Test ICMPv6Object.  Post, get, put, delete ICMPv6Object Objects.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    obj1 = fmcapi.ICMPv6Objects(fmc=fmc)
    obj1.name = "_icmpv6" + namer
    obj1.icmpType = "1"
    obj1.code = "0"
    obj1.post()

    obj1.get()
    obj1.code = "3"
    obj1.put()

    obj1.delete()

    logging.info("ICMPv6Object class done.\n")
