"""Moving the fmc.deploymentrequests to an actual api_object."""

import logging
from .deployabledevices import DeployableDevices
import datetime


class DeploymentRequests(
    object
):  # Can't import APIClassTemplate due to dependency loop.
    """
    Iterate through the list of devices needing deployed and submit a request to the FMC to deploy changes to them.

    :return:
    """

    URL_SUFFIX = "/deployment/deploymentrequests"

    def __init__(self, fmc):
        """
        Initialize DeploymentRequests object.

        :param fmc (object): FMC object
        :return: None
        """
        logging.debug("In __init__ for DeploymentRequests() class.")

        self.fmc = fmc
        self.URL = f"{self.fmc.configuration_url}{self.URL_SUFFIX}"
        self.uuids = None

    def get(self):
        """GET method for API for DeploymentRequests not supported."""
        logging.info("GET method for API for DeploymentRequests not supported.")

    def post(self):
        """
        Submit list of devices to FMC that need config changes pushed to them.

        :return: (list) List of devices.
        """
        logging.debug("In post() method for DeploymentRequests() class.")
        devices = DeployableDevices(fmc=self.fmc)
        self.uuids = devices.get()
        if not self.uuids:
            logging.info("No devices need deployed.")
            return
        json_data = {
            "type": "DeploymentRequest",
            "forceDeploy": True,
            "ignoreWarning": True,
            "version": str(int(1000000 * datetime.datetime.utcnow().timestamp())),
            "deviceList": [],
        }
        for device in self.uuids:
            logging.info(f"Adding device {device} to deployment queue.")
            json_data["deviceList"].append(device["device"]["id"])
            # From the list of deployable devices get the version value that is smallest.
            if int(json_data["version"]) > int(device["version"]):
                logging.info(f"Updating version to {device['version']}")
                json_data["version"] = device["version"]
        logging.info("Deploying changes to devices.")
        response = self.fmc.send_to_api(
            method="post", url=self.URL, json_data=json_data
        )
        return response["deviceList"]

    def put(self):
        """PUT method for API for DeploymentRequests not supported."""
        logging.info("PUT method for API for DeploymentRequests not supported.")
        pass

    def delete(self):
        """DELETE method for API for DeploymentRequests not supported."""
        logging.info("DELETE method for API for DeploymentRequests not supported.")
        pass
