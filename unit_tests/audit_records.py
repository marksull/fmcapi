import logging
import fmcapi


def test__audit_records(fmc):
    logging.info("Testing AuditRecords() class.")
    tmp = fmcapi.AuditRecords(fmc=fmc)
    logging.info(tmp.get())
    logging.info("Testing AuditRecords() class done.\n")
