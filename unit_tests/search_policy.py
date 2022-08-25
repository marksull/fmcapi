import logging
import fmcapi


def test__policy(fmc):
    logging.info("Test Policy.  Get search results.")

    obj1 = fmcapi.Policy(fmc=fmc, filter='0.0.0.0')
    result = obj1.get()
    logging.info(f"Total items: {len(result['items'])}")

    logging.info("Test Policy done.\n")
