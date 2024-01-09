from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .dynamicobjects import DynamicObject
import logging


class DynamicObjectMappings(APIClassTemplate):
    """The Dynamic Object in the FMC."""

    VALID_JSON_DATA = ["add", "remove", "mappings", "type", "id","name"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/dynamicobjectmappings"
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    REQUIRED_FOR_POST = []
    obj_id = ""

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
        if "id" in kwargs:
            self.obj_id = kwargs["id"]

    def handle_mappings(self, action, value, name):
        """
        Associate mappings to dynamic object.

        :param action: (str) 'add', 'remove', or 'clear'
        :param dynamic_objects: (DynamicObject) Dynamic object to be mapped.
        """
        logging.debug("In mappings for dynamic object")

        dynamic_object = DynamicObject(fmc=self.fmc, name=name)
        response = dynamic_object.get()
        if response:
            new_obj = {
                "dynamicObject": {
                    "name": response["name"],
                    "id": response["id"],
                    "type": response["type"],
                },
                "mappings": value,
            }
            if action == "add":
                if "add" in self.__dict__:
                    self.add.append(new_obj)

                else:
                    self.add = [new_obj]

                logging.info(f"Adding mappings to Dynamic Object.")

            elif action == "remove":
                if "remove" in self.__dict__:
                    self.remove.append(new_obj)

                else:
                    self.remove = [new_obj]

                logging.info(f"Remove mappings to Dynamic Object.")

        else:
            logging.warning(
                f'Dynamic Object "{name}" is not found in FMC.  Cannot add mappings.'
            )

    def get(self):
        self.URL_SUFFIX = f"/object/dynamicobjects/{str(self.obj_id)}/mappings"
        super().__init__(self.fmc)
        return super().get()

    def put(self):
        self.URL_SUFFIX = f"/object/dynamicobjects/{str(self.obj_id)}/mappings"
        super().__init__(self.fmc)
        return super().put()

    def delete(self):
        self.URL_SUFFIX = f"/object/dynamicobjects/{str(self.obj_id)}/mappings"
        super().__init__(self.fmc)
        return super().delete()



