"""IPSec Settings Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .ftds2svpns import FTDS2SVPNs
from fmcapi.api_objects.object_services.ikev1ipsecproposals import IKEv1IpsecProposals
from fmcapi.api_objects.object_services.ikev2ipsecproposals import IKEv2IpsecProposals
import logging


class IPSecSettings(APIClassTemplate):
    """The IPSecSettings Object in the FMC."""

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "tfcPackets",
        "validateIncomingIcmpErrorMessage",
        "enableSaStrengthEnforcement",
        "perfectForwardSecrecy",
        "lifetimeSeconds",
        "doNotFragmentPolicy",
        "lifetimeKilobytes",
        "cryptoMapType",
        "ikeV2Mode",
        "enableRRI",
        "ikeV2IpsecProposal",
        "ikeV1IpsecProposal",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    FIRST_SUPPORTED_FMC_VERSION = "6.3"
    PREFIX_URL = "/policy/ftds2svpns"
    REQUIRED_FOR_POST = ["vpn_id"]

    def __init__(self, fmc, **kwargs):
        """
        Initialize IPSecSettings object.

        Set self.type to "IPSecSettings" and parse the kwargs.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IPSecSettings class.")
        self.parse_kwargs(**kwargs)
        self.type = "IPSecSettings"

    def vpn_policy(self, pol_name):
        """
        Associate a VPN Policy.

        :param pol_name: (str) Name of VPN Policy.
        :return: None
        """
        logging.debug("In vpn_policy() for IPSecSettings class.")
        ftd_s2s = FTDS2SVPNs(fmc=self.fmc)
        ftd_s2s.get(name=pol_name)
        if "id" in ftd_s2s.__dict__:
            self.vpn_id = ftd_s2s.id
            self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{self.vpn_id}/ipsecsettings"
            self.vpn_added_to_url = True
        else:
            logging.warning(
                f'FTD S2S VPN Policy "{pol_name}" not found.  Cannot set up IPSecSettings for FTDS2SVPNs Policy.'
            )

    def ipsec_policy(self, pol_name, version=1, action="add"):
        """
        Associate IPSec Policy.

        :param pol_name: (str) Name of IPSec Policy.
        :param version: (int) Version number.
        :param action: (str) 'add', 'remove', or 'clear'.
        """
        logging.debug("In ipsec_policy() for IPSecSettings class.")
        pol1 = None
        if version == 1:
            pol1 = IKEv1IpsecProposals(fmc=self.fmc)
        elif version == 2:
            pol1 = IKEv2IpsecProposals(fmc=self.fmc)
        else:
            logging.warning("Invalid version type specified.  Must be 1 or 2")
        pol1.get(name=pol_name)
        new_pol = None

        if action == "add":
            if "id" in pol1.__dict__ and version == 1:
                new_pol = {"id": pol1.id, "name": pol1.name, "type": pol1.type}
            elif "id" in pol1.__dict__ and version == 2:
                new_pol = {"id": pol1.id, "name": pol1.name, "type": pol1.type}

            if new_pol is None:
                logging.warning(
                    f'IKEv"{version}"IpsecProposal "{pol_name}" not found.  Cannot set up IPSecSettings Policy.'
                )
            else:
                if "version" == 1:
                    logging.info(f'Adding "{pol_name}" to ikeV1IpsecProposal.')
                    if "ikeV1IpsecProposal" in self.__dict__:
                        self.ikeV1IpsecProposal.append(new_pol)
                    else:
                        self.ikeV1IpsecProposal = [new_pol]
                elif "version" == 2:
                    logging.info(f'Adding "{pol_name}" to ikeV2IpsecProposal.')
                    if "ikeV2IpsecProposal" in self.__dict__:
                        self.ikeV2IpsecProposal.append(new_pol)
                    else:
                        self.ikeV2IpsecProposal = [new_pol]

        elif action == "remove":
            if "version" == 1:
                if "ikeV1IpsecProposal" in self.__dict__:
                    self.ikeV1IpsecProposal = list(
                        filter(lambda i: i["name"] != pol_name, self.ikeV1IpsecProposal)
                    )
                else:
                    logging.warning(
                        "ikeV1IpsecProposal has no members.  Cannot remove policy."
                    )
            if "version" == 2:
                if "ikeV2IpsecProposal" in self.__dict__:
                    self.ikeV2IpsecProposal = list(
                        filter(lambda i: i["name"] != pol_name, self.ikeV2IpsecProposal)
                    )
                else:
                    logging.warning(
                        "ikeV2IpsecProposal has no members.  Cannot remove policy."
                    )

        elif action == "clear":
            if "version" == 1:
                if "ikeV1IpsecProposal" in self.__dict__:
                    del self.ikeV1IpsecProposal
            if "version" == 2:
                if "ikeV2IpsecProposal" in self.__dict__:
                    del self.ikeV2IpsecProposal
