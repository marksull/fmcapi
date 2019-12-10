"""Moving the fmc.deployabledevices to an actual api_object."""

import logging
import time


class DeployableDevices(
    object
):  # Can't import APIClassTemplate due to dependency loop.
    """
    Collect a list of FMC managed devices whose configuration is not up-to-date.

    :return: List of devices needing updates.
    """

    URL_SUFFIX = "/deployment/deployabledevices?expanded=true"
    WAIT_TIME = 15

    def __init__(self, fmc):
        """
        Initialize DeployableDevices object.

        :param fmc (object): FMC object
        :return: None
        """
        logging.debug("In __init__ for DeployableDevices() class.")

        logging.info(
            f"Waiting {self.WAIT_TIME} seconds to allow the FMC to update the list of deployable devices."
        )
        time.sleep(self.WAIT_TIME)

        self.fmc = fmc
        self.URL = f"{self.fmc.configuration_url}{self.URL_SUFFIX}"

    def get(self):
        """
        Use GET API call to query FMC for a list of devices that need configuration updates pushed to them.

        :return: (list) uuids
        """
        logging.debug("GET method for API for DeployableDevices.")
        logging.info("Getting a list of deployable devices.")
        response = self.fmc.send_to_api(method="get", url=self.URL)
        # Now to parse the response list to get the UUIDs of each device.
        if "items" not in response:
            return
        uuids = []
        for item in response["items"]:
            if not item["canBeDeployed"]:
                pass
            else:
                uuids.append(item)
        return uuids

    def post(self):
        """POST method for API for DeployableDevices not supported."""
        logging.info("POST method for API for DeployableDevices not supported.")
        pass

    def put(self):
        """PUT method for API for DeployableDevices not supported."""
        logging.info("PUT method for API for DeployableDevices not supported.")
        pass

    def delete(self):
        """DELETE method for API for DeployableDevices not supported."""
        logging.info("DELETE method for API for DeployableDevices not supported.")
        pass
