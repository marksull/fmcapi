import logging
import fmcapi


def test__application_risk(fmc):
    logging.info("Testing ApplicationRisk class.")

    obj1 = fmcapi.ApplicationRisks(fmc=fmc)
    logging.info("All ApplicationRisks -- >")
    result = obj1.get()
    logging.info(result)
    logging.info(f"Total items: {len(result['items'])}")

    del obj1
    obj1 = fmcapi.ApplicationRisks(fmc=fmc, name="Very High")
    logging.info("One ApplicationRisk -- >")
    logging.info(obj1.get())

    logging.info("Testing ApplicationRisk class done.\n")
