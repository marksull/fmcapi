from .apiclasstemplate import APIClassTemplate
import logging


class PortObjectGroup(APIClassTemplate):
    """
    The PortObjectGroup Object in the FMC.
    """

    URL_SUFFIX = '/object/portobjectgroups'

    # Technically you can have objects OR literals but I'm not set up for "OR" logic, yet.
    REQUIRED_FOR_POST = ['name', 'objects']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for PortObjectGroup class.")
        self.parse_kwargs(**kwargs)
        self.type = 'NetworkGroup'

    def format_data(self):
        logging.debug("In format_data() for PortObjectGroup class.")
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
        logging.debug("In parse_kwargs() for PortObjectGroup class.")
        if 'objects' in kwargs:
            self.objects = kwargs['objects']
        if 'literals' in kwargs:
            self.literals = kwargs['literals']

    def named_ports(self, action, name=''):
        logging.debug("In named_ports() for PortObjectGroup class.")
        if action == 'add':
            port1 = Ports(fmc=self.fmc)
            response = port1.get()
            if 'items' in response:
                new_port = None
                for item in response['items']:
                    if item['name'] == name:
                        new_port = {'name': item['name'], 'id': item['id'], 'type': item['type']}
                        break
                if new_port is None:
                    logging.warning('Port "{}" is not found in FMC.  Cannot add to PortObjectGroup.'.format(name))
                else:
                    if 'objects' in self.__dict__:
                        duplicate = False
                        for obj in self.objects:
                            if obj['name'] == new_port['name']:
                                duplicate = True
                                break
                        if not duplicate:
                            self.objects.append(new_port)
                            logging.info('Adding "{}" to PortObjectGroup.'.format(name))
                    else:
                        self.objects = [new_port]
                        logging.info('Adding "{}" to PortObjectGroup.'.format(name))
        elif action == 'remove':
            if 'objects' in self.__dict__:
                objects_list = []
                for obj in self.objects:
                    if obj['name'] != name:
                        objects_list.append(obj)
                self.objects = objects_list
                logging.info('Removed "{}" from PortObjectGroup.'.format(name))
            else:
                logging.info("This PortObjectGroup has no named_ports.  Nothing to remove.")
        elif action == 'clear':
            if 'objects' in self.__dict__:
                del self.objects
                logging.info('All named_ports removed from this PortObjectGroup.')
