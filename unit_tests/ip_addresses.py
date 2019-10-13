import logging
import fmcapi


def test__ip_addresses(fmc):
    logging.info("Test IPAddresses.  This only returns a full list of IP object types.")

    obj1 = fmcapi.NetworkAddresses(fmc=fmc)
    logging.info("IPAddresses -->")
    result = obj1.get()
    logging.info(result)

    logging.info("Test IPAddresses done.\n")
