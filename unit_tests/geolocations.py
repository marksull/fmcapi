import logging
import fmcapi


def test__geolocations(fmc):
    logging.info("Testing Geolocation class. Requires a configured Geolocation")

    obj1 = fmcapi.Geolocation(fmc=fmc)
    logging.info("All Geolocation -- >")
    result = obj1.get()
    logging.info(result)
    logging.info(f"Total items: {len(result['items'])}")
    del obj1

    obj1 = fmcapi.Geolocation(fmc=fmc, name="_tmp")
    logging.info("One Geolocation -- >")
    logging.info(obj1.get())

    logging.info("Testing Geolocation class done.\n")
