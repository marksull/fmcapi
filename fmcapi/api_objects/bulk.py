"""Class object to handle the bulk POST feature of FMC's API.  Only works for ACPRule BULK POSTs."""

import logging
import sys


class Bulk(object):
    """Bulk Class"""
    MAX_SIZE_QTY = 1000
    MAX_SIZE_IN_BYTES = 2048000
    REQUIRED_FOR_POST = []

    @property
    def URL_SUFFIX(self):
        """
        Add the URL suffixes for categories, insertBefore and insertAfter
        NOTE: You must specify these at the time the object is initialized (created) for this feature
        to work correctly. Example:
            This works:
                new_rule = ACPRule(fmc=fmc, acp_name='acp1', insertBefore=2)

            This does not:
                new_rule = ACPRule(fmc=fmc, acp_name='acp1')
                new_rule.insertBefore = 2
        """
        url = '?'

        if 'category' in self.__dict__:
            url = f'{url}category={self.category}&'
        if 'insertBefore' in self.__dict__:
            url = f'{url}insertBefore={self.insertBefore}&'
        if 'insertAfter' in self.__dict__:
            url = f'{url}insertAfter={self.insertAfter}&'
        if 'insertBefore' in self.__dict__ and 'insertAfter' in self.__dict__:
            logging.warning('ACP rule has both insertBefore and insertAfter params')
        if 'section' in self.__dict__:
            url = f'{url}section={self.section}&'

        return url[:-1]

    def __init__(self, fmc, url='', **kwargs):
        logging.debug("In __init__() for Bulk class.")
        self.fmc = fmc
        self.items = []
        self.URL = url
        self.parse_kwargs(**kwargs)

    def parse_kwargs(self, **kwargs):
        logging.debug("In parse_kwargs() for Bulk class.")
        if 'category' in kwargs:
            self.category = kwargs['category']
        if 'insertBefore' in kwargs:
            self.insertBefore = kwargs['insertBefore']
        if 'insertAfter' in kwargs:
            self.insertAfter = kwargs['insertAfter']
        if 'section' in kwargs:
            self.section = kwargs['section']

    def add(self, item):
        self.items.append(item)
        logging.info(f"Adding {item} to bulk items list.")

    def post(self):
        # Build URL
        self.URL = f'{self.URL}{self.URL_SUFFIX}&bulk=true'

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
