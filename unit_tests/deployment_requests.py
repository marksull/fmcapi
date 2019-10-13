import logging
import fmcapi


def test__deployment_requests(fmc):
    logging.info("Testing DeploymentRequests() class.")
    tmp = fmcapi.DeploymentRequests(fmc=fmc)
    logging.info(tmp.post())
    logging.info("Testing DeploymentRequests() class done.\n")
