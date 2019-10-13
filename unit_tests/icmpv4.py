import logging
import fmcapi
import time


def test__icmpv4(fmc):
    logging.info("Test ICMPv4Object.  Post, get, put, delete ICMPv4Object Objects.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    obj1 = fmcapi.ICMPv4Objects(fmc=fmc)
    obj1.name = "_icmpv4" + namer
    obj1.icmpType = "3"
    obj1.code = "0"
    obj1.post()

    obj1.get()
    obj1.code = "3"
    obj1.put()

    obj1.delete()

    logging.info("ICMPv4Object class done.\n")
