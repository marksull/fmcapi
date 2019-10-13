import logging
import fmcapi


def test__application_type(fmc):
    logging.info("Testing ApplicationType class.")

    obj1 = fmcapi.ApplicationTypes(fmc=fmc)
    logging.info("All ApplicationType -- >")
    result = obj1.get()
    logging.info(result)
    logging.info(f"Total items: {len(result['items'])}")

    del obj1
    obj1 = fmcapi.ApplicationTypes(fmc=fmc, name="Server")
    logging.info("One ApplicationType -- >")
    logging.info(obj1.get())

    logging.info("Testing ApplicationType class done.\n")
