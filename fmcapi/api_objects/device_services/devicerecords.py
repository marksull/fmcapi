from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.policy_services.accesspolicies import AccessPolicies
from fmcapi.api_objects.status_services import TaskStatuses
import time
import logging
import warnings
import re


class DeviceRecords(APIClassTemplate):
    """
    The DeviceRecords Object in the FMC.
    """

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "hostName",
        "natID",
        "regKey",
        "license_caps",
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
    REQUIRED_FOR_POST = ["accessPolicy", "hostName", "regKey"]
    REQUIRED_FOR_PUT = ["id"]
    LICENSES = ["CONTROL", "PROTECT", "BASE", "MALWARE", "URLFilter", "THREAT", "VPN", "URL"]

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for DeviceRecords class.")
        self.parse_kwargs(**kwargs)

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for DeviceRecords class.")
        if "acp_name" in kwargs:
            self.acp(name=kwargs["acp_name"])

    def licensing(self, action, name="BASE"):
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

    def acp(self, name=""):
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
        task_completed_states = ["Success", "SUCCESS", "COMPLETED"]
        try:
            status = TaskStatuses(fmc=self.fmc, id=task["id"])
            current_status = status.get()
            """
            Task Status for new device registration behaves differently than other tasks
            On new device registration, a task is sent for the initial registration. After completion 
            the UUID is deleted without any change in task status. So we check to see if the object no longer exists
            to assume the registration is complete.  After registration, discovery of the device begins, but there is
            no way to check for this with a task status.  The device can't be modified during this time, but a new device
            registration can begin.

            OTOH, a device HA operation will update its status to "Success" on completion.  Hence the two different checks.
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

    def get(self, name:str):
        logging.debug("In get() for DeviceRecords class.")
        devices = super().get()
        output = []
        if name:
            output = list(filter(lambda x: re.match(f".*{name}.*",x['name'],re.I), devices['items']))
        else:
            output = devices['items']

        return output

    def post(self, **kwargs):
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


class Device(DeviceRecords):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn("Deprecated: Device() should be called via DeviceRecords().")
        super().__init__(fmc, **kwargs)
