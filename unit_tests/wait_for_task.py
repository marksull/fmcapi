import fmcapi
import time
import logging


def wait_for_task(fmc, task, wait_time=10):
    task_completed_states = ["Success", "SUCCESS", "COMPLETED"]
    try:
        status = fmcapi.TaskStatuses(fmc=fmc, id=task["id"])
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
