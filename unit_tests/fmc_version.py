import logging
import fmcapi


def test__fmc_version(fmc):
    logging.info('Testing fmc.version() method.  Getting version information information from FMC.')

    version_info = fmc.serverversion()
    logging.info('fmc.version() -- >')
    logging.info(version_info)

    logging.info('Testing fmc.version() done.\n')
