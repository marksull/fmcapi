from .apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.policy_services.accesscontrolpolicy import AccessControlPolicy
from fmcapi.api_objects.device_services.device import Device
from fmcapi.api_objects.device_ha_pair_services.devicehapairs import DeviceHAPairs
from fmcapi.api_objects.policy_services.ftdnatpolicy import FTDNatPolicy
import logging


class PolicyAssignments(APIClassTemplate):
    """
    The PolicyAssignments Object in the FMC.
    """
    REQUIRED_FOR_POST = ['targets', 'policy']
    REQUIRED_FOR_PUT = ['id', 'targets', 'policy']
    URL_SUFFIX = '/assignment/policyassignments'
    FILTER_BY_NAME = True

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for PolicyAssignments class.")
        self.parse_kwargs(**kwargs)
        self.type = "PolicyAssignment"

    def format_data(self):
        logging.debug("In format_data() for PolicyAssignments class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'targets' in self.__dict__:
            json_data['targets'] = self.targets
        if 'policy' in self.__dict__:
            json_data['policy'] = self.policy
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for PolicyAssignments class.")
        if 'targets' in kwargs:
            self.targets = kwargs['targets']
        if 'policy' in kwargs:
            self.policy = kwargs['policy']

    def ftd_natpolicy(self, name, devices):
        logging.debug("In ftd_natpolicy() for PolicyAssignments class.")
        targets = []
        pol1 = FTDNatPolicy(fmc=self.fmc)
        pol1.get(name=name)
        if 'id' in pol1.__dict__:
            self.policy = {"type": pol1.type, "name": pol1.name, "id": pol1.id}
        else:
            logging.warning(f'FTD NAT Policy {name} not found.  Cannot set up PolicyAssignment.')
        for device in devices:
            if device["type"] == 'device':
                dev1 = Device(fmc=self.fmc)
                dev1.get(name=device['name'])
            elif device["type"] == 'deviceHAPair':
                dev1 = DeviceHAPairs(fmc=self.fmc)
                dev1.get(name=device['name'])
            if 'id' in dev1.__dict__:
                logging.info(f'Adding "{dev1.name}" to targets for this FTDNat PolicyAssignment.')
                targets.append({"type": dev1.type, "id": dev1.id, "name": dev1.name})
            else:
                logging.warning(f"Device/DeviceHA {device['name']} not found.  Cannot add to PolicyAssignment.")
        self.targets = targets

    def accesspolicy(self, name, devices):
        logging.debug("In accesspolicy() for PolicyAssignments class.")
        targets = []
        pol1 = AccessControlPolicy(fmc=self.fmc)
        pol1.get(name=name)
        if 'id' in pol1.__dict__:
            self.policy = {"type": pol1.type, "name": pol1.name, "id": pol1.id}
        else:
            logging.warning(f'Access Control Policy {name} not found.  Cannot set up PolicyAssignment.')
        for device in devices:
            if device["type"] == 'device':
                dev1 = Device(fmc=self.fmc)
                dev1.get(name=device['name'])
            elif device["type"] == 'deviceHAPair':
                dev1 = DeviceHAPairs(fmc=self.fmc)
                dev1.get(name=device['name'])
            if 'id' in dev1.__dict__:
                logging.info(f'Adding "{dev1.name}" to targets for this Access Control Policy PolicyAssignment.')
                targets.append({"type": dev1.type, "id": dev1.id, "name": dev1.name})
            else:
                logging.warning(f"Device/DeviceHA {device['name']} not found.  Cannot add to PolicyAssignment.")
        self.targets = targets

    def delete(self):
        logging.info('DELETE method for API for PolicyAssignments not supported.')
        pass
