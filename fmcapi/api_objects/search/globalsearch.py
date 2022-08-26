from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class GlobalSearch(APIClassTemplate):
    """
    The GlobalSearch Object in the FMC.
    """

    VALID_JSON_DATA = ["id", "name", "type", "category", "links", "self"]
    VALID_FOR_KWARGS = ["filter"]
    VALID_CHARACTERS_FOR_NAME = """[ .\w\d_\-]"""
    URL_SUFFIX = "/search/global"
    REQUIRED_FOR_GET = ["filter"]
    FILTER_BY_NAME = True
    FIRST_SUPPORTED_FMC_VERSION = "7.0"

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for GlobalSearch class.")
        self.parse_kwargs(**kwargs)
        self.URL = f"{self.URL}?filter={self.filter}"

    def format_data(self):
        json_data = super().format_data()
        logging.debug("In format_data() for GlobalSearch class.")
        return json_data
