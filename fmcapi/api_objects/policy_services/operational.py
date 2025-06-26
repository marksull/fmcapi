from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging




class AccessControlPolicyClone(APIClassTemplate):
    """The Dynamic Object in the FMC."""

    VALID_JSON_DATA = ["policies"]
    VALID_FOR_KWARGS = ["policies"]
    URL_SUFFIX = "/policy/operational/clonepolicies"
    # VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""
    REQUIRED_FOR_POST = ["policies"]

    def __init__(self, fmc, **kwargs):
        """
        Initialize PolicyClone object.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for PolicyClone class.")
        self.parse_kwargs(**kwargs)
