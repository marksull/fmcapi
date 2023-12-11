from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class DynamicObject(APIClassTemplate):
    """The Dynamic Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "description", "type", "objectType"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/dynamicobjects"
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    VALID_GET_FILTERS = [
        "unusedOnly",
        "ids" "nameStartsWith",
    ]  # unusedOnly:Bool, "ids:id1,id2,..." ,nameStartsWith:String

    def __init__(self, fmc, **kwargs):
        """
        Initialize Dynamic Object.

        Set self.type to "DynamicObject" and parse the kwargs.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Dynamic Object class.")
        self.parse_kwargs(**kwargs)
        self.type = "DynamicObject"
