import logging


def test__audit(fmc):
    logging.info('Testing fmc.audit() method.')
    logging.info(fmc.audit())
    logging.info('Testing fmc.audit() method done.\n')
