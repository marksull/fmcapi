import logging
import fmcapi


def test__continent(fmc):
    logging.info("Testing Continent class.")

    obj1 = fmcapi.Continents(fmc=fmc)
    logging.info("All Continents -- >")
    result = obj1.get()
    logging.info(result)
    logging.info(f"Total items: {len(result['items'])}")
    logging.info("\n")
    del obj1
    obj1 = fmcapi.Continents(fmc=fmc, name="North America")
    logging.info("One Continent -- >")
    logging.info(obj1.get())
    logging.info("\n")

    logging.info("Testing Continent class done.\n")
