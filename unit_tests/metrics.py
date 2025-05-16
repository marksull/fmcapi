import logging
import fmcapi


def test__metrics(fmc):
    logging.info("Test Metrics.  Get Metrics.")

    obj1 = fmcapi.Metrics(fmc=fmc)
    metrics = obj1.get(
        deviceUUIDs="6255c614-352f-11ee-ab63-aead54c9541f",
        metric="vpn",
        startTime=1747228084,
        endTime=1747228084,
        step=1
    )
    del(obj1)

    logging.info("Test Metrics done.\n")