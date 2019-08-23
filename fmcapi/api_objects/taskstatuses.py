from .apiclasstemplate import APIClassTemplate
import logging


class TaskStatuses(APIClassTemplate):
    """
    The Task Status Object in the FMC.
    """

    URL_SUFFIX = '/job/taskstatuses'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for TaskStatuses class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for TaskStatuses class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for TaskStatuses class.")

    def post(self):
        logging.info('POST method for API for TaskStatuses not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for TaskStatuses not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for TaskStatuses not supported.')
        pass
