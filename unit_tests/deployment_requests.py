import logging
import fmcapi


def test__deployment_requests(fmc):
    logging.info("Testing DeploymentRequests() class.")
    tmp = fmcapi.DeploymentRequests(fmc=fmc)
    # Deployments default to force deploy all devices while ignoring all warnings

    # Deploy all devices with pending deployments
    resp = tmp.post()

    # Deploy a specific selection of devices instead of all of them
    # tmp.deploy_all = False
    # tmp.deploy_device_names = ['device1', 'device2']
    # resp = tmp.post()

    # Deploy without force or without ignoring warnings
    # tmp.forceDeploy = False
    # tmp.ignoreWarning = False
    # tmp.post()

    logging.info(resp)
    logging.info("Testing DeploymentRequests() class done.\n")
