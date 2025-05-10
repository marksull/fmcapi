import logging
import fmcapi


def test__tunneldetails(fmc):
    logging.info("Test TunnelDetails.  Get TunnelDetails.")

    obj1 = fmcapi.TunnelDetails(fmc=fmc, container_uuid="40A6B737-FDDC-0ed3-0000-000000000297") # Tunnel uuid not topology uuid
    tunnel_details = obj1.get()
    del obj1

    logging.info("Test TunnelDetails done.\n")