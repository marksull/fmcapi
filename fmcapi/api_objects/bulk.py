"""Class object to handle the bulk POST feature of FMC's API."""

import logging
from .acprule import ACPRule


class Bulk(object):
    """Bulk Class"""
    MAX_BULK_POST_SIZE = 1000
    REQUIRED_FOR_POST = []

    def __init__(self, fmc, url=''):
        logging.debug("In __init__() for Bulk class.")
        self.fmc = fmc
        self.items = []
        self.URL = f'{url}?&bulk=true'

    def add(self, item):
        self.items.append(item)
        logging.info(f"Adding {item} to bulk items list.")

    def post(self):
        # Break up the items into MAX_BULK_POST_SIZE chunks.
        chunks = [self.items[i * self.MAX_BULK_POST_SIZE:(i + 1) * self.MAX_BULK_POST_SIZE]
                  for i in range((len(self.items) + self.MAX_BULK_POST_SIZE - 1) // self.MAX_BULK_POST_SIZE)]

        # Post the chunks
        for item in chunks:
            response = self.fmc.send_to_api(method='post', url=self.URL, json_data=item)
            logging.info(f"Posting to bulk items.")
            return response
