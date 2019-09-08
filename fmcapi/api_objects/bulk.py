"""Class object to handle the bulk POST feature of FMC's API."""

import logging
import sys


class Bulk(object):
    """Bulk Class"""
    MAX_SIZE_QTY = 1000
    MAX_SIZE_IN_BYTES = 2048000
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
        chunks = [self.items[i * self.MAX_SIZE_QTY:(i + 1) * self.MAX_SIZE_QTY]
                  for i in range((len(self.items) + self.MAX_SIZE_QTY - 1) // self.MAX_SIZE_QTY)]

        # Post the chunks
        for item in chunks:
            # I'm not sure what to do about the max bytes right now so I'll just throw a warning message.
            if sys.getsizeof(item, 0) > self.MAX_SIZE_IN_BYTES:
                logging.warning(f"This chunk of the post is too large.  Please submit less items to be bulk posted.")
            response = self.fmc.send_to_api(method='post', url=self.URL, json_data=item)
            logging.info(f"Posting to bulk items.")
            return response
