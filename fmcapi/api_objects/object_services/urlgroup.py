from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .url import URL
import logging


class URLGroup(APIClassTemplate):
    """
    The URLGroup Object in the FMC.
    """

    URL_SUFFIX = '/object/urlgroups'

    # Technically you can have objects OR literals but I'm not set up for "OR" logic, yet.
    REQUIRED_FOR_POST = ['name', 'objects']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for URLGroup class.")
        self.parse_kwargs(**kwargs)
        self.type = 'URLGroup'

    def format_data(self):
        logging.debug("In format_data() for URLGroup class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'objects' in self.__dict__:
            json_data['objects'] = self.objects
        if 'literals' in self.__dict__:
            json_data['literals'] = self.literals
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for URLGroup class.")
        if 'objects' in kwargs:
            self.objects = kwargs['objects']
        if 'literals' in kwargs:
            self.literals = kwargs['literals']

    def named_urls(self, action, name=''):
        logging.debug("In named_urls() for URLGroup class.")
        if action == 'add':
            url1 = URL(fmc=self.fmc)
            response = url1.get()
            if 'items' in response:
                new_url = None
                for item in response['items']:
                    if item['name'] == name:
                        new_url = {'name': item['name'], 'id': item['id'], 'type': item['type']}
                        break
                if new_url is None:
                    logging.warning(f'URL "{name}" is not found in FMC.  Cannot add to URLGroup.')
                else:
                    if 'objects' in self.__dict__:
                        duplicate = False
                        for obj in self.objects:
                            if obj['name'] == new_url['name']:
                                duplicate = True
                                break
                        if not duplicate:
                            self.objects.append(new_url)
                            logging.info(f'Adding "{name}" to URLGroup.')
                    else:
                        self.objects = [new_url]
                        logging.info(f'Adding "{name}" to URLGroup.')
        elif action == 'remove':
            if 'objects' in self.__dict__:
                objects_list = []
                for obj in self.objects:
                    if obj['name'] != name:
                        objects_list.append(obj)
                self.objects = objects_list
                logging.info(f'Removed "{name}" from URLGroup.')
            else:
                logging.info("This URLGroup has no named_urls.  Nothing to remove.")
        elif action == 'clear':
            if 'objects' in self.__dict__:
                del self.objects
                logging.info('All named_urls removed from this URLGroup.')

    def unnamed_urls(self, action, value=''):
        logging.debug("In unnamed_urls() for URLGroup class.")
        if action == 'add':
            if value == '':
                logging.error('Value assignment required to add unamed_url to URLGroup.')
                return
            value_type = 'Url'
            new_literal = {'type': value_type, 'url': value}
            if 'literals' in self.__dict__:
                duplicate = False
                for obj in self.literals:
                    if obj['url'] == new_literal['url']:
                        duplicate = True
                        break
                if not duplicate:
                    self.literals.append(new_literal)
                    logging.info(f'Adding "{value}" to URLGroup.')
            else:
                self.literals = [new_literal]
                logging.info(f'Adding "{value}" to URLGroup.')
        elif action == 'remove':
            if 'literals' in self.__dict__:
                literals_list = []
                for obj in self.literals:
                    if obj['url'] != value:
                        literals_list.append(obj)
                self.literals = literals_list
                logging.info(f'Removed "{value}" from URLGroup.')
            else:
                logging.info("This URLGroup has no unnamed_urls.  Nothing to remove.")
        elif action == 'clear':
            if 'literals' in self.__dict__:
                del self.literals
                logging.info('All unnamed_urls removed from this URLGroup.')
