import logging
import fmcapi
import pprint
pp = pprint.PrettyPrinter(indent=4)


def test__url_category(fmc):
    logging.info('# Testing URLCategory class.')
    obj1 = fmcapi.URLCategory(fmc=fmc)
    print('All URLCategories -- >')
    result = obj1.get()
    pp.pprint(result)
    print(f"Total items: {len(result['items'])}")
    print('\n')
    del obj1
    obj1 = fmcapi.URLCategory(fmc=fmc, name='SPAM URLs')
    print('One URLCategory -- >')
    pp.pprint(obj1.get())
    print('\n')
    logging.info('# Testing URLCategory class done.\n')
