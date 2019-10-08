import logging
import fmcapi


def test__ports(fmc):
    logging.info(
        "Test Ports.  This only returns a full list of various Port object types."
    )

    obj1 = fmcapi.Ports(fmc=fmc)
    logging.info("Ports -->")
    result = obj1.get()
    logging.info(result)

    logging.info("Test Ports done.\n")
