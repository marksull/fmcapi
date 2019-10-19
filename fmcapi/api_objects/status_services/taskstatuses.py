from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class TaskStatuses(APIClassTemplate):
    """
    The Task Status Object in the FMC.
    """

    VALID_JSON_DATA = ["id", "name", "type"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    REQUIRED_FOR_GET = ["id"]
    URL_SUFFIX = "/job/taskstatuses"
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for TaskStatuses class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        logging.info("POST method for API for TaskStatuses not supported.")
        pass

    def put(self):
        logging.info("PUT method for API for TaskStatuses not supported.")
        pass

    def delete(self):
        logging.info("DELETE method for API for TaskStatuses not supported.")
        pass
