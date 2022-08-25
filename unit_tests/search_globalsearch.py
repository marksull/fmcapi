import logging
import fmcapi


def test__globalsearch(fmc):
    logging.info("Test GlobalSearch.  Get search results.")

    obj1 = fmcapi.GlobalSearch(fmc=fmc, filter='0.0.0.0')
    result = obj1.get()
    logging.info(f"Total items: {len(result['items'])}")

    logging.info("Test GlobalSearch done.\n")
