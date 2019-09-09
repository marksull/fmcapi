import logging
import fmcapi
import pprint
pp = pprint.PrettyPrinter(indent=4)


def test__ports(fmc):
    logging.info(
        '# Test Ports.  This only returns a full list of various Port object types.')
    obj1 = fmcapi.Ports(fmc=fmc)
    print('Ports -->')
    result = obj1.get()
    pp.pprint(result)
    print('\n')
    logging.info('# Test Ports done.\n')

