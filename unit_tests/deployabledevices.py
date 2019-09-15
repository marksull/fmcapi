import logging


def test__deployabledevices(fmc):
    logging.info('Testing fmc.deployabledevices() method.')
    logging.info(fmc.deployabledevices())
    logging.info('Testing fmc.deployabledevices() method done.\n')
