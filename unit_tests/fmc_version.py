import logging
import fmcapi
import pprint
pp = pprint.PrettyPrinter(indent=4)


def test__fmc_version(fmc):
    logging.info('Testing fmc.version() method.  Getting version information information from FMC.')

    version_info = fmc.version()
    print('fmc.version() -- >')
    pp.pprint(version_info)
    print('\n')

    logging.info('# Testing fmc.verson() done.')
