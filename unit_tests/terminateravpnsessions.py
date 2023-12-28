import logging
import fmcapi


def test__terminateravpnsessions(fmc):
    logging.info("Test TerminateRAVPNSessions. Requires an existing session id, user, or user+device id")
    logging.info("Terminating many sessions at once, like all sessions on a device, will likely require increasing fmc timeout")

    obj1 = fmcapi.TerminateRAVPNSessions(fmc=fmc)
    ######DIFFERENT TERMINATION METHODS##########
    # Terminate user/users on a specific deivce
    usernames_to_terminate = ['zlantztest']
    device_id = "5fceadc2-ffef-11ed-94e9-8f60148d3f9b"
    obj1.terminateBy = "USER"
    obj1.usernames = usernames_to_terminate
    obj1.deviceId = device_id

    # Terminate by specific session id
    # Currently have not found a reliable way of getting ravpnsession ids since there is no get methods for ravpnsessions
    # I have already complained about this to the BU
    # obj1.terminateBy = "SESSION"

    # Terminate all sessions on device
    # device_id = "5fceadc2-ffef-11ed-94e9-8f60148d3f9b"
    # obj1.terminateBy = "DEVICE"
    # obj1.deviceId = device_id

    result = obj1.post()
    logging.info(result)
    del(obj1)

    logging.info("Test TerminateRAVPNSessions done.\n")
