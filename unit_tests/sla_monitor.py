import logging
import fmcapi
import time


def test__slamonitor(fmc):
    logging.info("Test SLAMonitor.  Post, get, put, delete SLAMonitor Objects.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    sz1 = fmcapi.SecurityZones(fmc=fmc)
    sz1.name = "SZ-OUTSIDE1"
    sz1.interfaceMode = "ROUTED"
    sz1.post()
    time.sleep(1)

    sz2 = fmcapi.SecurityZones(fmc=fmc)
    sz2.name = "SZ-OUTSIDE2"
    sz2.interfaceMode = "ROUTED"
    sz2.post()
    time.sleep(1)

    obj1 = fmcapi.SLAMonitors(fmc=fmc)
    obj1.name = namer
    obj1.frequency = 30
    obj1.slaId = 1
    obj1.monitorAddress = "8.8.8.7"
    obj1.timeout = 5000
    obj1.threshold = 2
    obj1.noOfPackets = 1
    obj1.dataSize = 28
    obj1.tos = 1
    obj1.interfaces(names=["SZ-OUTSIDE1", "SZ-OUTSIDE2"])
    obj1.post()
    logging.info("SLAMonitor Post -->")
    logging.info(obj1.format_data())
    logging.info("\n")
    obj1.get(name=namer)
    obj1.monitorAddress = "8.8.8.8"
    obj1.put()
    logging.info("SLAMonitor Put -->")
    logging.info(obj1.format_data())
    logging.info("\n")
    time.sleep(1)
    obj1.delete()
    sz1.delete()
    sz2.delete()
