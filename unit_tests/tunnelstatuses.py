import logging
import fmcapi


def test__tunnelstatuses(fmc):
    logging.info("Test TunnelStatuses.  Get TunnelStatuses.")

    obj1 = fmcapi.TunnelStatuses(fmc=fmc)
    all_tunnel_statuses = obj1.get()
    del(obj1)

    obj2 = fmcapi.TunnelStatuses(fmc=fmc)
    obj2.id = "40A6B737-FDDC-0ed3-0000-000000000297"
    id_tunnel_status = obj2.get()
    del(obj2)

    logging.info("Test TunnelStatuses done.\n")