"""DeviceGroupRecords class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.device_services.devicerecords import DeviceRecords
from fmcapi.api_objects.device_ha_pair_services.ftddevicehapairs import FTDDeviceHAPairs
import logging


class DeviceGroupRecords(APIClassTemplate):
    """The DeviceGroupRecords Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "members"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/devicegroups/devicegrouprecords"

    def __init__(self, fmc, **kwargs):
        """
        Initialize DeviceGroupRecords object.

        Set self.type to "DeviceGroup" and parse the kwargs.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for DeviceGroupRecords class.")
        self.type = "DeviceGroup"
        self.parse_kwargs(**kwargs)

    def devices(self, action, members=[]):
        """
        Add/modify name to members field of DeviceGroupRecords object.

        :param action: (str) 'add', 'remove', or 'clear'
        :param membres: (list) List of members in group.
        :return: None
        """
        logging.debug("In devices() for DeviceGroupRecords class.")
        if action == "add":
            for member in members:
                if member["type"] == "device":
                    dev1 = DeviceRecords(fmc=self.fmc)
                    dev1.get(name=member["name"])
                elif member["type"] == "deviceHAPair":
                    dev1 = FTDDeviceHAPairs(fmc=self.fmc)
                    dev1.get(name=member["name"])
                if "id" in dev1.__dict__:
                    if "members" in self.__dict__:
                        self.members.append(
                            {"id": dev1.id, "type": dev1.type, "name": dev1.name}
                        )
                    else:
                        self.members = [
                            {"id": dev1.id, "type": dev1.type, "name": dev1.name}
                        ]
                    logging.info(
                        f'DeviceRecord "{dev1.name}" added to this DeviceGroupRecords object.'
                    )
                else:
                    logging.warning(
                        f"{member} not found.  Cannot add DeviceRecord to DeviceGroupRecords."
                    )
        elif action == "remove":
            if "members" in self.__dict__:
                for member in members:
                    if member["type"] == "device":
                        dev1 = DeviceRecords(fmc=self.fmc)
                        dev1.get(name=member["name"])
                    elif member["type"] == "deviceHAPair":
                        dev1 = FTDDeviceHAPairs(fmc=self.fmc)
                        dev1.get(name=member["name"])
                    if "id" in dev1.__dict__:
                        if member["type"] == "device":
                            self.members = list(
                                filter(lambda i: i["id"] != dev1.id, self.members)
                            )
                        elif member["type"] == "deviceHAPair":
                            devHA1 = FTDDeviceHAPairs(fmc=self.fmc)
                            devHA1.get(name=member["name"])
                            self.members = list(
                                filter(
                                    lambda i: i["id"] != devHA1.primary["id"],
                                    self.members,
                                )
                            )
                            self.members = list(
                                filter(
                                    lambda i: i["id"] != devHA1.secondary["id"],
                                    self.members,
                                )
                            )
                    else:
                        logging.warning(
                            f"DeviceRecord {member} not registered.  Cannot remove DeviceRecord"
                            f" from DeviceGroupRecords."
                        )
            else:
                logging.warning(
                    "DeviceGroupRecords has no members.  Cannot remove DeviceRecord."
                )
        elif action == "clear":
            if "members" in self.__dict__:
                del self.members
                logging.info(
                    "All device records removed from this DeviceGroupRecords object."
                )
