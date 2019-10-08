"""
Moving the fmc.deployabledevices to an actual api_object.
"""

import logging
import time


class DeployableDevices(
    object
):  # Can't import APIClassTemplate due to dependency loop.
    """
    Collect a list of FMC managed devices who's configuration is not up-to-date.
    :return: List of devices needing updates.
    """

    URL_SUFFIX = "/deployment/deployabledevices?expanded=true"
    WAIT_TIME = 15

    def __init__(self, fmc):
        logging.debug("In __init__ for DeployableDevices() class.")

        logging.info(
            f"Waiting {self.WAIT_TIME} seconds to allow the FMC to update the list of deployable devices."
        )
        time.sleep(self.WAIT_TIME)

        self.fmc = fmc
        self.URL = f"{self.fmc.configuration_url}{self.URL_SUFFIX}"

    def get(self):
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
        logging.info("POST method for API for DeployableDevices not supported.")
        pass

    def put(self):
        logging.info("PUT method for API for DeployableDevices not supported.")
        pass

    def delete(self):
        logging.info("DELETE method for API for DeployableDevices not supported.")
        pass
