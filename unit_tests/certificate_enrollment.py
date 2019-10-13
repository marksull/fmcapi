import logging
import fmcapi


def test__cert_enrollment(fmc):
    logging.info("Testing CertEnrollment class. Requires a CertEnrollment")

    obj1 = fmcapi.CertEnrollments(fmc=fmc)
    logging.info("All CertEnrollments -- >")
    result = obj1.get()
    logging.info(result)
    logging.info(f"Total items: {len(result['items'])}")
    del obj1

    logging.info("Testing CertEnrollment class done.\n")
