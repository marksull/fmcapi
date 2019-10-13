from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .ftds2svpns import FTDS2SVPNs
from fmcapi.api_objects.object_services.ikev1policies import IKEv1Policies
from fmcapi.api_objects.object_services.ikev2policies import IKEv2Policies
from fmcapi.api_objects.object_services.certenrollments import CertEnrollments
import logging


class IKESettings(APIClassTemplate):
    """
	The IKESettings Object in the FMC.
	"""

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "ikeV1Settings",
        "ikeV2Settings",
        "description",
        "version",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    FIRST_SUPPORTED_FMC_VERSION = "6.3"
    PREFIX_URL = "/policy/ftds2svpns"
    REQUIRED_FOR_POST = ["vpn_id"]

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IKESettings class.")
        self.parse_kwargs(**kwargs)
        self.type = "IKESetting"

    def vpn_policy(self, pol_name):
        logging.debug("In vpn_policy() for IKESettings class.")
        ftd_s2s = FTDS2SVPNs(fmc=self.fmc)
        ftd_s2s.get(name=pol_name)
        if "id" in ftd_s2s.__dict__:
            self.vpn_id = ftd_s2s.id
            self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{self.vpn_id}/ikesettings"
            self.vpn_added_to_url = True
        else:
            logging.warning(
                f'FTD S2S VPN Policy "{pol_name}" not found.  Cannot set up IKESettings for FTDS2SVPNs Policy.'
            )

    def ike_policy(self, pol_name, version=1):
        # ikev1 and ikv2 policy names can overlap
        logging.debug("In ike_policy() for IKESettings class.")
        pol1 = None
        if version == 1:
            pol1 = IKEv1Policies(fmc=self.fmc)
        elif version == 2:
            pol1 = IKEv2Policies(fmc=self.fmc)
        else:
            logging.warning("Invalid version type specified.  Must be between 1-2")
        pol1.get(name=pol_name)

        if "id" in pol1.__dict__ and version == 1:
            self.ikeV1Settings["policy"] = {
                "id": pol1.id,
                "name": pol1.name,
                "type": pol1.type,
            }
        elif "id" in pol1.__dict__ and version == 2:
            self.ikeV2Settings["policy"] = {
                "id": pol1.id,
                "name": pol1.name,
                "type": pol1.type,
            }
        else:
            logging.warning(
                f'IKEv"{version}"Policy "{pol_name}" not found.  Cannot set up IKESettings Policy.'
            )

    def certificate(self, cert_name, version=1):
        logging.debug("In certificate() for IKESettings class.")
        cert1 = CertEnrollments(fmc=self.fmc)
        cert1.get(name=cert_name)
        if "id" in cert1.__dict__ and version == 1:
            self.ikeV1Settings["authenticationType"] = "CERTIFICATE"
            self.ikeV1Settings["certificateAuth"] = {
                "name": cert1.name,
                "id": cert1.id,
                "type": cert1.type,
            }
        elif "id" in cert1.__dict__ and version == 2:
            self.ikeV2Settings["authenticationType"] = "CERTIFICATE"
            self.ikeV2Settings["certificateAuth"] = {
                "name": cert1.name,
                "id": cert1.id,
                "type": cert1.type,
            }
        else:
            logging.warning(
                f'Certificate "{cert_name}" not found.  Cannot set up IKESettings Policy.'
            )
