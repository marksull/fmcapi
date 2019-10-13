import logging
import fmcapi


def test__application(fmc):
    logging.info("Testing Application class.")

    obj1 = fmcapi.Applications(fmc=fmc)
    logging.info("All Application -- >")
    result = obj1.get(limit=1000)
    logging.info(result)
    logging.info(f"Total items: {len(result['items'])}")

    del obj1
    obj1 = fmcapi.Applications(fmc=fmc, name="WD softwares Download/Update")
    logging.info("One Application -- >")
    logging.info(obj1.get(limit=1000))

    logging.info("Testing Application class done.\n")
