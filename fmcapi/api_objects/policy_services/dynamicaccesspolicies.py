"""DynamicAccessPolicies Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import xmltodict
import base64


class DynamicAccessPolicies(APIClassTemplate):
    """The DynamicAccessPolicies Object in the FMC."""
    REQUIRED_FOR_PUT = [
        "id",
        "authorizationAttributes",
        "dapXmlConfig_dict",
        "hostscanXmlConfig_dict",
    ]
    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "authorizationAttributes",
        "dapXmlConfig",
        "hostscanXmlConfig",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/policy/dynamicaccesspolicies"
    FIRST_SUPPORTED_FMC_VERSION = "7.2"

    def __init__(self, fmc, **kwargs):
        """
        Initialize DynamicAccessPolicies object.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for DynamicAccessPolicies class.")
        self.type = "DynamicAccessPolicy"
        self.parse_kwargs(**kwargs)

    def unpack_xml_config(self, encoded_xml):

        """
        Unpack and reformat base64 encoded xml from DAP api responses

        Args:
            encoded_xml (string): base64 encoded xml string from either dapXmlConfig or hostscanXmlConfig

        Returns:
            dict: base64 decoded 'encoded_xml' represented as a dict instead of xml
        """

        decoded_xml = base64.b64decode(encoded_xml).decode("utf-8")
        xml_dict = xmltodict.parse(decoded_xml)

        return xml_dict

    def repack_xml_config(self, xml_dict):

        """Repack dict into xml and encoded for use with DAP api calls

        Args:
            xml_dict (_type_): _description_

        Returns:
            _type_: _description_
        """

        xml = xmltodict.unparse(xml_dict)
        encoded_xml_bytes = base64.b64encode(xml.encode("utf-8"))
        encoded_xml_string = encoded_xml_bytes.decode("utf-8")

        return encoded_xml_string

    def get(self, **kwargs):

        """
        Modified get() for DynamicAccessPolicies class to make working with
        dapXmlConfig and hostscanXmlConfig a bit easier. This will create self.dapXmlConfig_dict
        and self.hostscanXmlConfig_dict from the base64 encoded xml from the api repsonse.
        """

        super().get(**kwargs)
        logging.debug("In get() for DynamicAccessPolicies class.")
        if hasattr(self, 'dapXmlConfig'):
            self.dapXmlConfig_dict = self.unpack_xml_config(self.dapXmlConfig)

        if hasattr(self, 'hostscanXmlConfig'):
            self.hostscanXmlConfig_dict = self.unpack_xml_config(self.hostscanXmlConfig)

    def post(self, **kwargs):

        """
        Modified post() for DynamicAccessPolicies class to make working with
        dapXmlConfig and hostscanXmlConfig a bit easier. This will take self.dapXmlConfig_dict
        and self.hostscanXmlConfig_dict and convert to xml before base64 encoding for use with api endpoint.
        """

        if hasattr(self, 'dapXmlConfig_dict'):
            self.dapXmlConfig = self.repack_xml_config(self.dapXmlConfig_dict)

        if hasattr(self, 'hostscanXmlConfig_dict'):
            self.hostscanXmlConfig = self.repack_xml_config(self.hostscanXmlConfig_dict)

        super().post(**kwargs)
        logging.debug("In post() for DynamicAccessPolicies class.")

    def put(self, **kwargs):

        """
        Modified put() for DynamicAccessPolicies class to make working with
        dapXmlConfig and hostscanXmlConfig a bit easier. This will take self.dapXmlConfig_dict
        and self.hostscanXmlConfig_dict and convert to xml before base64 encoding for use with api endpoint.
        """

        if hasattr(self, 'dapXmlConfig_dict'):
            self.dapXmlConfig = self.repack_xml_config(self.dapXmlConfig_dict)

        if hasattr(self, 'hostscanXmlConfig_dict'):
            self.hostscanXmlConfig = self.repack_xml_config(self.hostscanXmlConfig_dict)

        super().put(**kwargs)
        logging.debug("In put() for DynamicAccessPolicies class.")
