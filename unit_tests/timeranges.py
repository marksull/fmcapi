import logging
import fmcapi
import time

def test__timeranges(fmc):
    logging.info("Testing TimeRanges class.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    time_range = fmcapi.TimeRanges(fmc=fmc)
    time_range.name = namer
    time_range.effectiveStartDateTime = "1979-01-01T00:00"
    time_range.effectiveEndDateTime = "1979-01-01T00:01"
    time_range.post()
    time_range.get()
    time_range.effectiveStartDateTime = "1979-01-02T00:00"
    time_range.effectiveEndDateTime = "1979-01-02T00:01"
    time_range.put()
    time_range.delete()

    logging.info("Testing TimeRanges class done.\n")