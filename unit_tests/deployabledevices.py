import logging


def test__deployabledevices(fmc):
    logging.info('Testing fmc.deployabledevices() method.')
    logging.info(fmc.deployabledevices())
    logging.info(fmc.get_deployable_devices())
    logging.info('Testing fmc.deployabledevices() method done.\n')
