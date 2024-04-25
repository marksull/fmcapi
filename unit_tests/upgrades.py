import logging
import fmcapi
import time
from .wait_for_task import wait_for_task


def test__upgrades(fmc):
    logging.info(
        """Test UpgradePackages/ApplicableDevices/Upgrades with Task.
        This will copy the listed upgrade file to registered devices

        Commented lines at the bottom show how to trigger readiness check, the actual upgrade process,
        and the post upgrade deployment.

        NOTE: this script will do this to ALL applicable devices based on the package_name given.
            example: you have 5 FTDvs and you only want to upgrade 2 of them. Input here is just the package_name.
            Script will add all eligible devices for the particular file given to the list of devices to run against.
            Potentially resulting in upgrading all 5 FTDv unintentionally.
        """
    )

    package_name = "Cisco_FTD_Patch-7.4.1.1-12.sh.REL.tar"
    device_list = []

    logging.info("All UpgradePackages -- >")
    package1 = fmcapi.UpgradePackages(fmc=fmc)
    result = package1.get()
    logging.info(result)
    del package1

    package1 = fmcapi.UpgradePackages(fmc=fmc, name=package_name)
    logging.info("One UpgradePackage -- >")
    logging.info(package1.get())

    applicable1 = fmcapi.ListApplicableDevices(fmc=fmc)
    applicable1.upgrade_package(package_name=package_name)
    time.sleep(1)
    result = applicable1.get()
    devices = result.get("items", [])

    for device in devices:
        device_list.append(device["name"])

    upgrades1 = fmcapi.Upgrades(fmc=fmc)
    upgrades1.devices(devices=device_list)
    upgrades1.upgrade_package(package_name=package_name)
    upgrades1.pushUpgradeFileOnly = True

    logging.info(f"Pushing upgrade file to {device_list}")
    response = upgrades1.post()
    logging.info(response)
    wait_for_task(fmc=fmc, task=response["metadata"]["task"], wait_time=60)

    # BELOW ARE EXAMPLES OF HOW TO TRIGGER READINESS CHECKS AND ACTUAL UPGRADES
    # THIS INCLUDES REBOOTS AND DEPLOYMENTS.

    # upgrades1.pushUpgradeFileOnly = False
    # upgrades1.readinessCheckOnly = True

    # logging.info(f"Triggering readiness checks on {device_list}")
    # response = upgrades1.post()
    # logging.info(response)
    # wait_for_task(fmc=fmc, task=response["metadata"]["task"], wait_time=60)

    # upgrades1.readinessCheckOnly = False

    # logging.info(f"Triggering REAL UPGRADE on {device_list}")
    # response = upgrades1.post()
    # logging.info(response)
    # wait_for_task(fmc=fmc, task=response["metadata"]["task"], wait_time=60)

    # logging.info(f"Upgrade completed. Triggering deployment to devices")
    # deployment = fmcapi.DeploymentRequests(fmc=fmc)
    # logging.info(deployment)
    # wait_for_task(fmc=fmc, task=deployment["metadata"]["task"], wait_time=60)

    logging.info("Test UpgradePackages/ApplicableDevices/Upgrades Complete")
