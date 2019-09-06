"""Class object to handle the bulk POST feature of FMC's API."""

import logging
from .acprule import ACPRule


class Bulk(object):
    """Bulk Class"""
    MAX_BULK_POST_SIZE = 1000

    def __init__(self, fmc, class_type='ACPRule', url_suffix=''):
        logging.debug("In __init__() for Bulk class.")
        self.fmc = fmc
        self.items = []
        self.class_type = class_type  # ACPRule is the only class that supports bulk but let's not assume that forever.
        self.URL = ''
        if self.class_type is 'ACPRule':
            self.URL = f'{ACPRule.URL}?{url_suffix}&bulk=true'

    def add(self, item):
        valid = False
        if self.class_type is 'ACPRule':
            if ACPRule.valid_for_post(item):
                valid = True

        if valid:
            self.items.append(item)
            logging.info(f"Adding {item} to bulk items list.")
        else:
            logging.info(f"Unable to add {item}.  Didn't pass valid_for_post().")

    def post(self):
        # Break up the items into MAX_BULK_POST_SIZE chunks.
        chunks = [self.items[i * self.MAX_BULK_POST_SIZE:(i + 1) * self.MAX_BULK_POST_SIZE]
                  for i in range((len(self.items) + self.MAX_BULK_POST_SIZE - 1) // self.MAX_BULK_POST_SIZE)]

        # Post the chunks
        for item in chunks:
            response = self.fmc.send_to_api(method='post', url=self.URL, json_data=item)
            logging.info(f"Posting to bulk items.")
            return response
