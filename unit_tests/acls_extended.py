import logging
import fmcapi


def test__extended_acls(fmc):
    logging.info(
        "Testing ExtendedAccessList class. Requires a configured ExtendedAccessList"
    )

    obj1 = fmcapi.ExtendedAccessList(fmc=fmc)
    logging.info("All ExtendedAccessList -- >")
    result = obj1.get()
    logging.info(result)
    logging.info(f"Total items: {len(result['items'])}")
    del obj1

    logging.info("Testing ExtendedAccessList class done.\n")
