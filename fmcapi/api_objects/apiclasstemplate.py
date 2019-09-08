"""Super class that is inherited by all API objects."""
from .helper_functions import *
import logging

logging.debug(f"In the {__name__} module.")


class APIClassTemplate(object):
    """
    This class is the base framework for all the objects in the FMC.
    """

    REQUIRED_FOR_POST = ['name']
    REQUIRED_FOR_PUT = ['id']
    REQUIRED_FOR_DELETE = ['id']
    FILTER_BY_NAME = False
    URL = ''
    URL_SUFFIX = ''
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-]"""

    @property
    def show_json(self):
        return self.format_data()

    def __init__(self, fmc, **kwargs):
        logging.debug("In __init__() for APIClassTemplate class.")
        self.fmc = fmc
        self.URL = f'{self.fmc.configuration_url}{self.URL_SUFFIX}'

    def parse_kwargs(self, **kwargs):
        logging.debug("In parse_kwargs() for APIClassTemplate class.")
        if 'bulk' in kwargs:
            self.bulk = kwargs['bulk']
        if 'limit' in kwargs:
            self.limit = kwargs['limit']
        else:
            self.limit = self.fmc.limit
        if 'offset' in kwargs:
            self.offset = kwargs['offset']
        if 'name' in kwargs:
            self.name = syntax_correcter(kwargs['name'], permitted_syntax=self.VALID_CHARACTERS_FOR_NAME)
            if self.name != kwargs['name']:
                logging.info(f"Adjusting name '{kwargs['name']}' to '{self.name}' due to invalid characters.")
        if 'description' in kwargs:
            self.description = kwargs['description']
        else:
            self.description = 'Created by fmcapi.'
        if 'metadata' in kwargs:
            self.metadata = kwargs['metadata']
        if 'overridable' in kwargs:
            self.overridable = kwargs['overridable']
        else:
            self.overridable = False
        if 'type' in kwargs:
            self.type = kwargs['type']
        if 'links' in kwargs:
            self.links = kwargs['links']
        if 'paging' in kwargs:
            self.paging = kwargs['paging']
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'items' in kwargs:
            self.items = kwargs['items']

    def valid_for_post(self):
        logging.debug("In valid_for_post() for APIClassTemplate class.")
        for item in self.REQUIRED_FOR_POST:
            if item not in self.__dict__:
                return False
        return True

    def valid_for_put(self):
        logging.debug("In valid_for_put() for APIClassTemplate class.")
        for item in self.REQUIRED_FOR_PUT:
            if item not in self.__dict__:
                return False
        return True

    def valid_for_delete(self):
        logging.debug("In valid_for_delete() for APIClassTemplate class.")
        for item in self.REQUIRED_FOR_DELETE:
            if item not in self.__dict__:
                return False
        return True

    def post(self, **kwargs):
        logging.debug("In post() for APIClassTemplate class.")
        if 'id' in self.__dict__:
            logging.info("ID value exists for this object.  Redirecting to put() method.")
            self.put()
        else:
            if self.valid_for_post():
                response = self.fmc.send_to_api(method='post', url=self.URL, json_data=self.format_data())
                if response:
                    self.parse_kwargs(**response)
                    if 'name' in self.__dict__ and 'id' in self.__dict__:
                        logging.info(f'POST success. Object with name: "{self.name}" and id: "{id}" created in FMC.')
                    else:
                        logging.info('POST success but no "id" or "name" values in API response.')
                else:
                    logging.warning('POST failure.  No data in API response.')
                return response
            else:
                logging.warning("post() method failed due to failure to pass valid_for_post() test.")
                return False

    def format_data(self):
        logging.debug("In format_data() for APIClassTemplate class.")

    def get(self, **kwargs):
        """
        If no self.name or self.id exists then return a full listing of all objects of this type.
        Otherwise set "expanded=true" results for this specific object.
        :return:
        """
        logging.debug("In get() for APIClassTemplate class.")
        self.parse_kwargs(**kwargs)
        if 'id' in self.__dict__:
            url = f'{self.URL}/{self.id}'
            response = self.fmc.send_to_api(method='get', url=url)
            self.parse_kwargs(**response)
            if 'name' in self.__dict__:
                logging.info(f'GET success. Object with name: "{self.name}" and id: "{self.id}" fetched from FMC.')
            else:
                logging.info(f'GET success. Object with id: "{self.id}" fetched from FMC.')
        elif 'name' in self.__dict__:
            if self.FILTER_BY_NAME:
                url = f'{self.URL}?name={self.name}&expanded=true'
            else:
                url = f'{self.URL}?expanded=true'
                if 'limit' in self.__dict__:
                    url = f'{url}&limit={self.limit}'
                if 'offset' in self.__dict__:
                    url = f'{url}&offset={self.offset}'
            response = self.fmc.send_to_api(method='get', url=url)
            if 'items' not in response:
                response['items'] = []
            for item in response['items']:
                if 'name' in item:
                    if item['name'] == self.name:
                        self.id = item['id']
                        self.parse_kwargs(**item)
                        logging.info(f'GET success. Object with name: "{self.name}" and id: "{self.id}" '
                                     f'fetched from FMC.')
                        return item
                else:
                    logging.warning(f'No "name" attribute associated with this item to check against {self.name}.')
            if 'id' not in self.__dict__:
                logging.warning(f"\tGET query for {self.name} is not found.\n\t\tResponse: {json.dumps(response)}")
        else:
            logging.info("GET query for object with no name or id set.  "
                         "Returning full list of these object types instead.")
            url = f'{self.URL}?expanded=true&limit={self.limit}'
            response = self.fmc.send_to_api(method='get', url=url)
        if 'items' not in response:
            response['items'] = []
        return response

    def put(self, **kwargs):
        logging.debug("In put() for APIClassTemplate class.")
        self.parse_kwargs(**kwargs)
        if self.valid_for_put():
            url = f'{self.URL}/{self.id}'
            response = self.fmc.send_to_api(method='put', url=url, json_data=self.format_data())
            self.parse_kwargs(**response)
            if 'name' in self.__dict__:
                logging.info(f'PUT success. Object with name: "{self.name}" and id: "{self.id}" updated in FMC.')
            else:
                logging.info(f'PUT success. Object with id: "{self.id}" updated in FMC.')
            return response
        else:
            logging.warning("put() method failed due to failure to pass valid_for_put() test.")
            return False

    def delete(self, **kwargs):
        logging.debug("In delete() for APIClassTemplate class.")
        self.parse_kwargs(**kwargs)
        if self.valid_for_delete():
            url = f'{self.URL}/{self.id}'
            response = self.fmc.send_to_api(method='delete', url=url, json_data=self.format_data())
            if not response:
                return None
            self.parse_kwargs(**response)
            if 'name' in self.name:
                logging.info(f'DELETE success. Object with name: "{self.name}" and id: "{self.id}" deleted in FMC.')
            else:
                logging.info(f'DELETE success. Object id: "{self.id}" deleted in FMC.')
            return response
        else:
            logging.warning("delete() method failed due to failure to pass valid_for_delete() test.")
            return False
