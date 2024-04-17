"""Time Ranges Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class TimeRanges(APIClassTemplate):
    """The TimeRanges Object in the FMC."""

    VALID_JSON_DATA = [
        "id",
        "name",
        "description",
        "effectiveStartDateTime",
        "effectiveEndDateTime",
        "recurrenceList"
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    REQUIRED_FOR_POST = [
        "name",
        "effectiveStartDateTime",
        "effectiveEndDateTime"
    ]
    URL_SUFFIX = "/object/timeranges"

    def __init__(self, fmc, **kwargs):
        """
        Initialize TimeRanges object.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for TimeRanges class.")
        self.parse_kwargs(**kwargs)
