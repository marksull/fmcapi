import logging
import fmcapi


def test__object(fmc):
    logging.info("Test Object.  Get search results.")

    obj1 = fmcapi.Object(fmc=fmc, filter='0.0.0.0')
    result = obj1.get()
    logging.info(f"Total items: {len(result['items'])}")

    logging.info("Test Object done.\n")
