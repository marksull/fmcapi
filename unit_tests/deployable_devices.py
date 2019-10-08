import logging
import fmcapi


def test__deployable_devices(fmc):
    logging.info("Testing DeployableDevices() class.")
    tmp = fmcapi.DeployableDevices(fmc=fmc)
    logging.info(tmp.get())
    logging.info("Testing DeployableDevices() method done.\n")
