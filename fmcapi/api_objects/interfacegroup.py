from .apiclasstemplate import APIClassTemplate
from .physicalinterface import PhysicalInterface
import logging


class InterfaceGroup(APIClassTemplate):
    """
    The InterfaceGroup Object in the FMC.
    """

    URL_SUFFIX = '/object/interfacegroups'
    REQUIRED_FOR_POST = ['name', 'interfaceMode']
    REQUIRED_FOR_PUT = ['id']
    FILTER_BY_NAME = True

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for InterfaceGroup class.")
        self.parse_kwargs(**kwargs)
        self.type = 'InterfaceGroup'

    def format_data(self):
        logging.debug("In format_data() for InterfaceGroup class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'description' in self.__dict__:
            json_data['description'] = self.description
        if 'interfaceMode' in self.__dict__:
            json_data['interfaceMode'] = self.interfaceMode
        if 'interfaces' in self.__dict__:
            json_data['interfaces'] = self.interfaces
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for InterfaceGroup class.")
        if 'interfaceMode' in kwargs:
            self.interfaceMode = kwargs['interfaceMode']
        else:
            self.interfaceMode = 'ROUTED'
        if 'interfaces' in kwargs:
            self.interfaces = kwargs['interfaces']

    def p_interface(self, device_name="", action="add", names=[]):
        logging.debug("In interfaces() for InterfaceGroup class.")
        if action == 'add':
            intfs = []
            for name in names:
                intf = PhysicalInterface(fmc=self.fmc)
                intf.get(name=name, device_name=device_name)
                if 'id' in intf.__dict__ and 'ifname' in intf.__dict__:
                    intfs.append({'name': intf.name, 'id': intf.id, 'type': intf.type})
                elif 'id' in intf.__dict__:
                    logging.warning(
                        'PhysicalInterface, "{}", found without logical ifname.  Cannot add to InterfaceGroup.'
                        .format(name))
                else:
                    logging.warning(
                        'PhysicalInterface, "{}", not found.  Cannot add to InterfaceGroup.'.format(name))
            if len(intfs) != 0:
                # Make sure we found at least one intf
                self.interfaces = intfs
            else:
                logging.warning(
                    'No valid PhysicalInterface found: "{}".  Cannot remove from InterfaceGroup.'.format(names))
        elif action == 'remove':
            if 'interfaces' in self.__dict__:
                intfs = []
                for interface in self.interfaces:
                    if interface["name"] not in names:
                        intfs.append(interface)
                    else:
                        logging.info('Removed "{}" from InterfaceGroup.'.format(interface["name"]))
                self.interfaces = intfs
            else:
                logging.warning("This InterfaceObject has no interfaces.  Nothing to remove.")
        elif action == 'clear-all':
            if 'interfaces' in self.__dict__:
                del self.interfaces
                logging.info('All PhysicalInterfaces removed from this InterfaceGroup.')
