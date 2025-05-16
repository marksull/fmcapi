import logging
import fmcapi


def test__events(fmc):
    logging.info("Test Events.  Get Events.")

    obj1 = fmcapi.Events(fmc=fmc)
    events = obj1.get()
    del(obj1)

    logging.info("Test Events done.\n")