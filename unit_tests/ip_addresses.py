import logging
import fmcapi
import pprint
pp = pprint.PrettyPrinter(indent=4)


def test__ip_addresses(fmc):
    logging.info('Test IPAddresses.  This only returns a full list of IP object types.')

    obj1 = fmcapi.IPAddresses(fmc=fmc)
    print('IPAddresses -->')
    result = obj1.get()
    pp.pprint(result)
    print('\n')

    logging.info('# Test IPAddresses done.\n')
