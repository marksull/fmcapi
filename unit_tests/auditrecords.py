import logging


def test__auditrecords(fmc):
    logging.info('Testing fmc.auditrecords() method.')
    logging.info(fmc.audit())
    logging.info(fmc.auditrecords())
    logging.info('Testing fmc.auditrecords() method done.\n')
