import logging
import fmcapi


def test__application_filter(fmc):
    logging.info("Testing ApplicationFilter class.")
    obj1 = fmcapi.ApplicationFilters(fmc=fmc)
    logging.info("All ApplicationFilters -- >")
    result = obj1.get()
    logging.info(result)
    # There are no Application Filters by default so there is no items in the list.
    if "items" in result:
        logging.info(f"Total items: {len(result['items'])}")
    del obj1

    logging.info("Testing ApplicationFilter class done.\n")
