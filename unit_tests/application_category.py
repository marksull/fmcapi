import logging
import fmcapi


def test__application_category(fmc):
    logging.info("Testing ApplicationCategory class.")

    obj1 = fmcapi.ApplicationCategories(fmc=fmc)
    logging.info("All ApplicationCategories -- >")
    result = obj1.get()
    logging.info(result)
    logging.info(f"Total items: {len(result['items'])}")
    logging.info("\n")
    del obj1
    obj1 = fmcapi.ApplicationCategories(fmc=fmc, name="SMS tools")
    logging.info("One ApplicationCategory -- >")
    logging.info(obj1.get())
    logging.info("\n")

    logging.info("Testing ApplicationCategory class done.\n")
