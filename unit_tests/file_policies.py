import logging
import fmcapi


def test__filepolicies(fmc):
    logging.info("Testing FilePolicies class.")

    obj1 = fmcapi.FilePolicies(fmc=fmc)
    logging.info("All FilePolicies -- >")
    result = obj1.get()
    logging.info(result)
    logging.info(f"Total items: {len(result['items'])}")

    del obj1

    logging.info("Testing FilePolicies class done.\n")
