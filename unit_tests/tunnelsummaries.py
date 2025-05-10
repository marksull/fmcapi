import logging
import fmcapi


def test__tunnelsummaries(fmc):
    logging.info("Test TunnelSummaries.  Get TunnelSummaries.")

    obj1 = fmcapi.TunnelSummaries(fmc=fmc)
    tunnel_summaries = obj1.get()
    del obj1

    logging.info("Test TunnelSummaries done.\n")