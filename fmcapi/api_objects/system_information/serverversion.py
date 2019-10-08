"""
Moving the fmc.serverversion to an actual api_object.
"""

import logging


class ServerVersion(object):  # Can't import APIClassTemplate due to dependency loop.
    """
    Get the FMC's version information.  Set instance variables for each version info returned as well as return
    the whole response text.
    :return:
    """

    URL_SUFFIX = "/info/serverversion"

    def __init__(self, fmc):
        logging.debug("In __init__() for ServerVersion class.")

        self.fmc = fmc
        self.URL = f"{self.fmc.platform_url}{self.URL_SUFFIX}"
        self.vdbVersion = None
        self.sruVersion = None
        self.serverVersion = None
        self.geoVersion = None

    def get(self):
        logging.debug("GET method for API for ServerVersion.")
        response = self.fmc.send_to_api(method="get", url=self.URL)
        if "items" in response:
            logging.info(
                "Populating vdbVersion, sruVersion, serverVersion, and geoVersion FMC instance variables."
            )
            self.vdbVersion = response["items"][0]["vdbVersion"]
            self.sruVersion = response["items"][0]["sruVersion"]
            self.serverVersion = response["items"][0]["serverVersion"]
            self.geoVersion = response["items"][0]["geoVersion"]
        return response

    def post(self):
        logging.info("POST method for API for ServerVersion not supported.")
        pass

    def put(self):
        logging.info("PUT method for API for ServerVersion not supported.")
        pass

    def delete(self):
        logging.info("DELETE method for API for ServerVersion not supported.")
        pass
