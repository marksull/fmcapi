import logging
import fmcapi
import time
from unit_tests import wait_for_task
import pprint
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
