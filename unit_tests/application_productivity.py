import logging
import fmcapi


def test__application_productivity(fmc):
    logging.info("Testing ApplicationProductivity class.")

    obj1 = fmcapi.ApplicationProductivities(fmc=fmc)
    logging.info("All ApplicationProductivities -- >")
    result = obj1.get()
    logging.info(result)
    logging.info(f"Total items: {len(result['items'])}")
    logging.info("\n")
    del obj1
    obj1 = fmcapi.ApplicationProductivities(fmc=fmc, name="Very Low")
    logging.info("One ApplicationProductivity -- >")
    logging.info(obj1.get())

    logging.info("Testing ApplicationProductivity class done.\n")
