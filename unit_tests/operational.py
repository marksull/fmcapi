import logging
import fmcapi
import time


def test__acp_clone(fmc):
    logging.info("Test AccessControlPolicy clone.  .")

    obj1 = fmcapi.AccessControlPolicyClone(fmc=fmc, policies=[{
            "id": "EC01D571-D99E-0ed3-0000-292057822510",
            "type": "AccessPolicy",
            "cloneName": "Clone-test",}])
    result = obj1.post()

