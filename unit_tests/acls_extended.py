import logging
import fmcapi
import pprint
pp = pprint.PrettyPrinter(indent=4)


def test__extended_acls(fmc):
    logging.info('Testing ExtendedAccessList class. Requires a configured ExtendedAccessList')

    obj1 = fmcapi.ExtendedAccessList(fmc=fmc)
    print('All ExtendedAccessList -- >')
    result = obj1.get()
    pp.pprint(result)
    print(f"Total items: {len(result['items'])}")
    del obj1

    logging.info('# Testing ExtendedAccessList class done.\n')
