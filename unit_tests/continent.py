import logging
import fmcapi
import pprint
pp = pprint.PrettyPrinter(indent=4)


def test__continent(fmc):
    logging.info('Testing Continent class.')

    obj1 = fmcapi.Continent(fmc=fmc)
    print('All Continents -- >')
    result = obj1.get()
    pp.pprint(result)
    print(f"Total items: {len(result['items'])}")
    print('\n')
    del obj1
    obj1 = fmcapi.Continent(fmc=fmc, name='North America')
    print('One Continent -- >')
    pp.pprint(obj1.get())
    print('\n')

    logging.info('Testing Continent class done.\n')
