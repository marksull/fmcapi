"""Device Records Classes."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.policy_services.accesspolicies import AccessPolicies
from fmcapi.api_objects.status_services import TaskStatuses
import time
import logging


class DeviceRecords(APIClassTemplate):
    """The DeviceRecords Object in the FMC."""

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "hostName",
        "natID",
        "regKey",
        "license_caps",
        "performanceTier",
        "accessPolicy",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + [
        "acp_name",
        "acp_id",
        "model",
        "modelId",
        "modelNumber",
        "modelType",
        "healthStatus",
        "healthPolicy",
        "type",
        "version",
        "sw_version",
        "deviceGroup",
        "prohibitPacketTransfer",
        "keepLocalEvents",
        "ftdMode",
        "keepLocalEvents",
    ]
    URL_SUFFIX = "/devices/devicerecords"
    REQUIRED_FOR_POST = ["accessPolicy", "hostName", "regKey", "type"]
    REQUIRED_FOR_PUT = ["id"]
    LICENSES = [
        "BASE",
        "THREAT",
        "URLFilter",
        "MALWARE",
        "APEX",
        "PLUS",
        "VPNOnly",
        "INSTANCE",
    ]
    TIERS = ["FTDv5", "FTDv10", "FTDv20", "FTDv30", "FTDv50", "FTDv100", "Legacy"]

    def __init__(self, fmc, **kwargs):
        """
        Initialize DeviceRecords object.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for DeviceRecords class.")
        self.parse_kwargs(**kwargs)

    def parse_kwargs(self, **kwargs):
        """
        Parse the kwargs and set self variables to match.

        :return: None
        """
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for DeviceRecords class.")
        if "acp_name" in kwargs:
            self.acp(name=kwargs["acp_name"])

    def licensing(self, action, name="BASE"):
        """
        Associate licenses with this device record.

        :param action: (str) 'add', 'remove', 'clear'
        :param name: (str) Value from LICENSES constant.
        :return: None
        """
        logging.debug("In licensing() for DeviceRecords class.")
        if action == "add":
            if name in self.LICENSES:
                if "license_caps" in self.__dict__:
                    self.license_caps.append(name)
                    self.license_caps = list(set(self.license_caps))
                else:
                    self.license_caps = [name]
                logging.info(f'License "{name}" added to this DeviceRecords object.')

            else:
                logging.warning(
                    f"{name} not found in {self.LICENSES}.  Cannot add license to DeviceRecords."
                )
        elif action == "remove":
            if name in self.LICENSES:
                if "license_caps" in self.__dict__:
                    try:
                        self.license_caps.remove(name)
                    except ValueError:
                        logging.warning(
                            f"{name} is not assigned to this devicerecord thus cannot be removed."
                        )
                    logging.info(
                        f'License "{name}" removed from this DeviceRecords object.'
                    )
                else:
                    logging.warning(
                        f"{name} is not assigned to this devicerecord thus cannot be removed."
                    )

            else:
                logging.warning(
                    f"{name} not found in {self.LICENSES}.  Cannot remove license from DeviceRecords."
                )
        elif action == "clear":
            if "license_caps" in self.__dict__:
                del self.license_caps
                logging.info("All licensing removed from this DeviceRecords object.")

    def tiering(self, action, name=""):
        """
        Associate performance tier with this device record.

        :param action: (str) 'add', 'remove', 'clear'
        :param name: (str) Value from TIERS constant.
        :return: None
        """
        logging.debug("In tiering() for DeviceRecords class.")
        if self.fmc.serverVersion < "7.0":
            logging.warning(
                f"FTD performance tier licenses are supported only in FMC version 7.0 and newer."
            )
        else:
            if action == "add":
                if name in self.TIERS:
                    self.performanceTier = name
                    logging.info(
                        f'Performance tier "{name}" added to this DeviceRecords object.'
                    )
                else:
                    logging.warning(
                        f"{name} not found in {self.TIERS}.  Cannot add performance tier to DeviceRecords."
                    )
            elif action == "remove":
                if name in self.TIERS:
                    if "performanceTier" in self.__dict__:
                        try:
                            self.performanceTier = ""
                        except ValueError:
                            logging.warning(
                                f"{name} performance tier cannot be removed."
                            )
                        logging.info(
                            f'License "{name}" removed from this DeviceRecords object.'
                        )
                    else:
                        logging.warning(
                            f"{name} is not assigned to this DeviceRecords thus cannot be removed."
                        )

                else:
                    logging.warning(
                        f"{name} not found in {self.TIERS}.  Cannot remove performance tier from DeviceRecords."
                    )
            elif action == "clear":
                if "performanceTier" in self.__dict__:
                    del self.performanceTier
                    logging.info(
                        "Performance tier removed from this DeviceRecords object."
                    )

    def acp(self, name=""):
        """
        Associate AccessPolicy with this device.

        :param name: (str) Name of ACP.
        :return: None
        """
        logging.debug("In acp() for DeviceRecords class.")
        acp = AccessPolicies(fmc=self.fmc)
        acp.get(name=name)
        if "id" in acp.__dict__:
            self.accessPolicy = {"id": acp.id, "type": acp.type}
        else:
            logging.warning(
                f"Access Control Policy {name} not found.  Cannot set up accessPolicy for DeviceRecords."
            )

    def wait_for_task(self, task, wait_time=10):
        """
        Pause configuration script and wait for device registration to complete.

        :param task: (dict) task["id": (str)]
        :param wait_time: (int) Seconds to wait before rechecking.
        :return: None
        """
        task_completed_states = ["Success", "SUCCESS", "COMPLETED"]
        try:
            status = TaskStatuses(fmc=self.fmc, id=task["id"])
            current_status = status.get()
            """
            Task Status for new device registration behaves differently than other tasks
            On new device registration, a task is sent for the initial registration. After completion
            the UUID is deleted without any change in task status. So we check to see if the object no longer exists
            to assume the registration is complete.  After registration, discovery of the device begins, but there is
            no way to check for this with a task status.  The device can't be modified during this time, but a new
            device registration can begin.

            OTOH, a device HA operation will update its status to "Success" on completion.  Hence the two different
            checks.
            """
            while (
                current_status["status"] is not None
                and current_status["status"] not in task_completed_states
            ):
                # Lot of inconsistencies with the type of data a task can return
                if "taskType" in current_status.keys():
                    logging.info(
                        f"Task: {current_status['taskType']} {current_status['status']} {current_status['id']}"
                    )
                    time.sleep(wait_time)
                    current_status = status.get()
                else:
                    logging.info(
                        f"Task: {current_status['status']} {current_status['id']}"
                    )
                    time.sleep(wait_time)
                    current_status = status.get()
            logging.info(f"Task: {current_status['status']} {current_status['id']}")
        except Exception as e:
            logging.info(type(e), e)

    def post(self, **kwargs):
        """POST to FMC API."""
        logging.debug("In post() for DeviceRecords class.")
        response = super().post(**kwargs)
        #  self.wait_for_task(task=response["metadata"]["task"], wait_time=30)  # Doesn't work yet.
        if "post_wait_time" in kwargs:
            self.post_wait_time = kwargs["post_wait_time"]
        else:
            self.post_wait_time = 300
        logging.info(
            f"DeviceRecords registration task submitted.  "
            f"Waiting {self.post_wait_time} seconds for it to complete."
        )
        time.sleep(self.post_wait_time)
        return response
