import logging
import fmcapi


def test__application_tag(fmc):
    logging.info("Testing ApplicationTag class.")

    obj1 = fmcapi.ApplicationTags(fmc=fmc)
    logging.info("All ApplicationTag -- >")
    result = obj1.get()
    logging.info(result)
    logging.info(f"Total items: {len(result['items'])}")

    del obj1
    obj1 = fmcapi.ApplicationTags(fmc=fmc, name="file sharing/transfer")
    logging.info("One ApplicationTag -- >")
    logging.info(obj1.get())

    logging.info("Testing ApplicationTag class done.\n")
