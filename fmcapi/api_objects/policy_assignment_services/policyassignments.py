"""Policy Assignements Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.policy_services.accesspolicies import AccessPolicies
from fmcapi.api_objects.device_services.devicerecords import DeviceRecords
from fmcapi.api_objects.device_ha_pair_services.ftddevicehapairs import FTDDeviceHAPairs
from fmcapi.api_objects.policy_services.ftdnatpolicies import FTDNatPolicies
import logging


class PolicyAssignments(APIClassTemplate):
    """The PolicyAssignments Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "type", "targets", "policy"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    REQUIRED_FOR_POST = ["targets", "policy"]
    REQUIRED_FOR_PUT = ["id", "targets", "policy"]
    URL_SUFFIX = "/assignment/policyassignments"
    FILTER_BY_NAME = True

    def __init__(self, fmc, **kwargs):
        """
        Initialize PolicyAssignments object.

        Set self.type to "PolicyAssignment", parse the kwargs, and set up the self.URL.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for PolicyAssignments class.")
        self.parse_kwargs(**kwargs)
        self.type = "PolicyAssignment"

    def ftd_natpolicy(self, name, devices):
        """
        Associate FTD NAT Policy with a list of devices.

        :param name: (str) Name of FTD NAT Policy.
        :param devices: (list) List of device names.
        """
        logging.debug("In ftd_natpolicy() for PolicyAssignments class.")
        targets = []
        pol1 = FTDNatPolicies(fmc=self.fmc)
        pol1.get(name=name)
        if "id" in pol1.__dict__:
            self.policy = {"type": pol1.type, "name": pol1.name, "id": pol1.id}
        else:
            logging.warning(
                f"FTD NAT Policy {name} not found.  Cannot set up PolicyAssignment."
            )
        for device in devices:
            if device["type"] == "device":
                dev1 = DeviceRecords(fmc=self.fmc)
                dev1.get(name=device["name"])
            elif device["type"] == "deviceHAPair":
                dev1 = FTDDeviceHAPairs(fmc=self.fmc)
                dev1.get(name=device["name"])
            if "id" in dev1.__dict__:
                logging.info(
                    f'Adding "{dev1.name}" to targets for this FTDNat PolicyAssignment.'
                )
                targets.append({"type": dev1.type, "id": dev1.id, "name": dev1.name})
            else:
                logging.warning(
                    f"Device/DeviceHA {device['name']} not found.  Cannot add to PolicyAssignment."
                )
        self.targets = targets

    def accesspolicy(self, name, devices):
        """
        Assign Access Control Policy to the list of devices.

        :param name: (str) Name of ACP.
        :param devices: (list) List of device names.
        """
        logging.debug("In accesspolicy() for PolicyAssignments class.")
        targets = []
        pol1 = AccessPolicies(fmc=self.fmc)
        pol1.get(name=name)
        if "id" in pol1.__dict__:
            self.policy = {"type": pol1.type, "name": pol1.name, "id": pol1.id}
        else:
            logging.warning(
                f"Access Control Policy {name} not found.  Cannot set up PolicyAssignment."
            )
        for device in devices:
            if device["type"] == "device":
                dev1 = DeviceRecords(fmc=self.fmc)
                dev1.get(name=device["name"])
            elif device["type"] == "deviceHAPair":
                dev1 = FTDDeviceHAPairs(fmc=self.fmc)
                dev1.get(name=device["name"])
            if "id" in dev1.__dict__:
                logging.info(
                    f'Adding "{dev1.name}" to targets for this Access Control Policy PolicyAssignment.'
                )
                targets.append({"type": dev1.type, "id": dev1.id, "name": dev1.name})
            else:
                logging.warning(
                    f"Device/DeviceHA {device['name']} not found.  Cannot add to PolicyAssignment."
                )
        self.targets = targets

    def delete(self):
        """DELETE method for API for PolicyAssignments not supported."""
        logging.info("DELETE method for API for PolicyAssignments not supported.")
        pass
