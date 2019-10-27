import logging
import fmcapi


def test__fmc_version(fmc):
    logging.info(
        "Testing ServerVersion() method.  Getting version information information from FMC."
    )

    version_info = fmcapi.ServerVersion(fmc=fmc)
    logging.info(version_info.get())
    logging.info("Testing ServerVersion() done.\n\n")
