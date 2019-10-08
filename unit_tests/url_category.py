import logging
import fmcapi


def test__url_category(fmc):
    logging.info("Testing URLCategory class.")
    obj1 = fmcapi.URLCategories(fmc=fmc)
    logging.info("All URLCategories -- >")
    result = obj1.get()
    logging.info(result)
    logging.info(f"Total items: {len(result['items'])}")

    del obj1
    obj1 = fmcapi.URLCategories(fmc=fmc, name="SPAM URLs")
    logging.info("One URLCategory -- >")
    logging.info(obj1.get())

    logging.info("Testing URLCategory class done.\n")
