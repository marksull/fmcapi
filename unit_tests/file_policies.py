import logging
import fmcapi
import pprint
pp = pprint.PrettyPrinter(indent=4)


def test__filepolicies(fmc):
    logging.info('Testing FilePolicies class.')

    obj1 = fmcapi.FilePolicies(fmc=fmc)
    print('All FilePolicies -- >')
    result = obj1.get()
    pp.pprint(result)
    print(f"Total items: {len(result['items'])}")
    print('\n')
    del obj1

    logging.info('Testing FilePolicies class done.\n')
