import logging
import fmcapi


def test__staticroutes(fmc):
    logging.info("Testing StaticRoutes class. Requires a registered device")

    obj1 = fmcapi.StaticRoutes(fmc=fmc)
    obj1.device(device_name="device_name")
    logging.info("All StaticRoutes -- >")
    result = obj1.get()
    logging.info(result)
    logging.info(f"Total items: {len(result['items'])}")

    del obj1

    logging.info("Testing StaticRoutes class done.\n")
