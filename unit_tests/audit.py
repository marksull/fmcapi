import logging
import pprint
pp = pprint.PrettyPrinter(indent=4)


def test__audit(fmc):
    logging.info('# Testing fmc.audit() method.')
    pp.pprint(fmc.audit())
    logging.info('# Testing fmc.audit() method done.\n')
