import logging
import fmcapi
import pprint
import time
pp = pprint.PrettyPrinter(indent=4)


def test__upgrades(fmc):
    logging.info(
        '# Test UpgradePackages/ApplicableDevices/Upgrades with Task.'
        '  This will copy the listed upgrade file to registered devices')

    package_name = 'Cisco_FTD_Patch-6.3.0.3-77.sh.REL.tar'
    device_list = []

    print('All UpgradePackages -- >')
    package1 = fmcapi.UpgradePackage(fmc=fmc)
    result = package1.get()
    pp.pprint(result)
    del package1

    package1 = fmcapi.UpgradePackage(fmc=fmc, name=package_name)
    print('One UpgradePackage -- >')
    pp.pprint(package1.get())

    applicable1 = fmcapi.ApplicableDevices(fmc=fmc)
    applicable1.upgrade_package(package_name=package_name)
    time.sleep(1)
    result = applicable1.get()
    devices = result.get('items', [])

    for device in devices:
        device_list.append(device['name'])

    upgrades1 = fmcapi.Upgrades(fmc=fmc)
    upgrades1.devices(devices=device_list)
    upgrades1.upgrade_package(package_name=package_name)
    upgrades1.pushUpgradeFileOnly = True

    response = upgrades1.post()
    pp.pprint(response)
    wait_for_task(fmc=fmc, task=response["metadata"]["task"], wait_time=60)

    logging.info('# Test UpgradePackages/ApplicableDevices/Upgrades Complete')


def wait_for_task(fmc, task, wait_time=10):
    task_completed_states = ['Success', 'SUCCESS', 'COMPLETED']
    try:
        status = fmcapi.TaskStatuses(fmc=fmc, id=task["id"])
        current_status = status.get()
        '''
        Task Status for new device registration behaves differently than other tasks
        On new device registration, a task is sent for the initial registration. After completion 
        the UUID is deleted without any change in task status. So we check to see if the object no longer exists
        to assume the registration is complete.  After registration, discovery of the device begins, but there is
        no way to check for this with a task status.  The device can't be modified during this time, but a new device
        registration can begin.

        OTOH, a device HA operation will update its status to "Success" on completion.  Hence the two different checks.
        '''
        while current_status["status"] is not None and current_status["status"] not in task_completed_states:
            # Lot of inconsistencies with the type of data a task can return
            if 'taskType' in current_status.keys():
                print("Task: %s %s %s" % (
                    current_status["taskType"], current_status["status"], current_status["id"]))
                time.sleep(wait_time)
                current_status = status.get()
            else:
                print("Task: %s %s" % (
                    current_status["status"], current_status["id"]))
                time.sleep(wait_time)
                current_status = status.get()
        print("Task: %s %s" % (
            current_status["status"], current_status["id"]))
    except Exception as e:
        print(type(e), e)
