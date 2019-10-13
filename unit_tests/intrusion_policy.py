import logging
import fmcapi


def test__intrusion_policy(fmc):
    logging.info("Test IntrusionPolicy. Can only GET IntrusionPolicy objects.")
    obj1 = fmcapi.IntrusionPolicies(fmc=fmc)
    obj1.get(name="Security Over Connectivity")
    logging.info("IntrusionPolicy -->")
    logging.info(obj1.format_data())

    logging.info("Test IntrusionPolicy done.\n")
