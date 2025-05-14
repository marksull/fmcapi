import logging
import fmcapi


def test__alerts(fmc):
    logging.info("Test Alerts.  Get Alerts.")

    obj1 = fmcapi.Alerts(fmc=fmc)
    alerts = obj1.get()
    del(obj1)

    logging.info("Test Alerts done.\n")