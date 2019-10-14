"""
Misc methods/functions that are used by the fmcapi package's modules.
"""

import re
import ipaddress
import json
import logging
from .status_services import TaskStatuses
import time

logging.debug(f"In the {__name__} module.")


def wait_for_task(fmc, task, wait_time=10):
    task_completed_states = ["Success", "SUCCESS", "COMPLETED"]
    try:
        status = TaskStatuses(fmc=fmc, id=task["id"])
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
                    "Task: %s %s %s"
                    % (
                        current_status["taskType"],
                        current_status["status"],
                        current_status["id"],
                    )
                )
                time.sleep(wait_time)
                current_status = status.get()
            else:
                logging.info(
                    "Task: %s %s" % (current_status["status"], current_status["id"])
                )
                time.sleep(wait_time)
                current_status = status.get()
        logging.info("Task: %s %s" % (current_status["status"], current_status["id"]))
    except Exception as e:
        logging.info(type(e), e)


def syntax_correcter(value, permitted_syntax="""[.\w\d_\-]""", replacer="_"):
    """
    Check 'value' for invalid characters (identified by 'permitted_syntax') and replace them with 'replacer'.
    :param value:  String to be checked.
    :param permitted_syntax: (optional) regex of allowed characters.
    :param replacer: (optional) character used to replace invalid characters.
    :return: Modified string with "updated" characters.
    """
    logging.debug("In syntax_correcter() helper_function.")
    new_value = ""
    for char in range(0, len(value)):
        if not re.match(permitted_syntax, value[char]):
            new_value += replacer
        else:
            new_value += value[char]
    return new_value


def get_networkaddress_type(value):
    """
    Check to see whether 'value' is a host, range, or network.
    :param value: 
    :return: 'host'/'network'/'range'
    """
    logging.debug("In get_networkaddress_type() helper_function.")
    if "/" in value:
        ip, bitmask = value.split("/")
        if ip == "32" or bitmask == "128":
            return "host"
        else:
            return "network"
    else:
        if "-" in value:
            return "range"
        else:
            return "host"


def is_ip(ip):
    """
    Checks to see whether the provided string is an IP address.
    :param ip: String
    :return: True/False
    """
    logging.debug("In is_ip() helper_function.")
    try:
        ipaddress.ip_address(ip)
    except ValueError as err:
        logging.error(err)
        return False
    return True


def is_ip_network(ip):
    """
    Checks to see whether the provided string is a valid network address.  That is, it checks to see if the
     provided IP/SM is the "network address" of the subnet.
    :param ip: String
    :return: True/False
    """
    logging.debug("In is_ip_network() helper_function.")
    try:
        ipaddress.ip_network(ip)
    except ValueError as err:
        logging.error(err)
        return False
    return True


def validate_ip_bitmask_range(value="", value_type=""):
    """
    We need to check the provided IP address (or range of addresses) and make sure the IPs are valid.
    :param value: IP, IP/Bitmask, or IP Range
    :param value_type: 'host'/'network'/'range'
    :return: dict {value=value_fixed, valid=boolean}
    """
    logging.debug("In validate_ip_bitmask_range() helper_function.")
    return_dict = {"value": value, "valid": False}
    if value_type == "range":
        for ip in value.split("-"):
            if is_ip(ip):
                return_dict["valid"] = True
    elif value_type == "host" or value_type == "network":
        if is_ip_network(value):
            return_dict["valid"] = True
    return return_dict["valid"]


def mocked_requests_get(**kwargs):
    """
    Use to "mock up" a response from using the "requests" library to avoid actually using the "requests" library.
    :param kwargs: 
    :return: 
    """
    logging.debug("In mocked_requests_get() helper_function.")

    class MockResponse:
        def __init__(self, **kwargs):
            logging.debug("In MockResponse __init__ method.")
            self.text = json.dumps(kwargs["text"])
            self.status_code = kwargs["status_code"]

        def close(self):
            logging.debug("In MockResponse close method.")
            return True

    return MockResponse(**kwargs)


def validate_vlans(start_vlan, end_vlan=""):
    logging.debug("In validate_vlans() helper_function.")
    if end_vlan == "":
        end_vlan = start_vlan
    if int(end_vlan) < int(start_vlan):
        start_vlan, end_vlan = end_vlan, start_vlan
    if 0 < int(start_vlan) < 4095 and 0 < int(end_vlan) < 4095:
        return start_vlan, end_vlan
    else:
        return 1, 4094
