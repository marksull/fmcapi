"""Misc methods/functions that are used by the fmcapi package's modules."""

import re
import ipaddress
import json
import logging
import uuid


logging.debug(f"In the {__name__} module.")


PROTOCOL_MAP = {
    "TCP": "6",
    "UDP": "17",
    "ICMP": "1",
    "IGMP": "2",
    "GGP": "3",
    "IP": "0",
    "ST": "5",
    "EGP": "8",
    "IGP": "9",
    "BBN-RCC-MON": "10",
    "NVP-II": "11",
    "PUP": "12",
    "ARGUS": "13",
    "EMCON": "14",
    "XNET": "15",
    "CHAOS": "16",
    "MUX": "18",
    "DCN-MEAS": "19",
    "HMP": "20",
    "PRM": "21",
    "XNS-IDP": "22",
    "TRUNK-1": "23",
    "TRUNK-2": "24",
    "LEAF-1": "25",
    "LEAF-2": "26",
    "RDP": "27",
    "IRTP": "28",
    "ISO-TP4": "29",
    "NETBLT": "30",
    "MFE-NSP": "31",
    "MERIT-INP": "32",
    "DCCP": "33",
    "3PC": "34",
    "IDPR": "35",
    "XTP": "36",
    "DDP": "37",
    "IDPR-CMTP": "38",
    "TP": "39",
    "IL": "40",
    "IPV6": "41",
    "SDRP": "42",
    "ROUTING": "43",
    "FRAGMENT": "44",
    "IDRP": "45",
    "RSVP": "46",
    "GRE": "47",
    "DSR": "48",
    "BNA": "49",
    "ESP": "50",
    "AH": "51",
    "I-NLSP": "52",
    "SWIPE": "53",
    "NARP": "54",
    "MOBILE": "55",
    "TLSP": "56",
    "SKIP": "57",
    "ICMPV6": "58",
    "NONE": "59",
    "DSTOPTS": "60",
    "AHIP": "61",
    "CFTP": "62",
    "ALN": "63",
    "SAT-EXPAK": "64",
    "KRYPTOLAN": "65",
    "RVD": "66",
    "IPPC": "67",
    "AFS": "71",
    "SAT-MON": "69",
    "VISA": "70",
    "IPCV": "72",
    "CPNX": "73",
    "CPHB": "74",
    "WSN": "75",
    "PVP": "76",
    "BR-SAT-MON": "77",
    "SUN-ND": "78",
    "WB-MON": "79",
    "WB-EXPAK": "80",
    "ISO-IP": "81",
    "VMTP": "81",
    "SECURE-VMTP": "82",
    "VINES": "83",
    "TTP": "84",
    "IPTM": "84",
    "NSFNET-IGP": "85",
    "DGP": "86",
    "TCF": "87",
    "EIGRP": "88",
    "OSPFIGP": "89",
    "SPRITE-RPC": "90",
    "LARP": "91",
    "MTP": "92",
    "AX.25": "93",
    "IPIP": "94",
    "MICP": "95",
    "SCC-SP": "96",
    "ETHERIP": "97",
    "ENCAP": "98",
    "ENCRYPT": "99",
    "AIM": "100",
    "GMTP": "100",
    "IFMP": "101",
    "PNNI": "102",
    "PIM": "103",
    "ARIS": "104",
    "SCPS": "105",
    "QNX": "106",
    "A/N": "107",
    "IPCOMP": "108",
    "SNP": "109",
    "COMPAQ-PEER": "110",
    "IPX-IN-IP": "111",
    "VRRP": "112",
    "PGM": "113",
    "0HOP": "114",
    "L2TP": "115",
    "DDX": "116",
    "IATP": "117",
    "STP": "118",
    "SRP": "119",
    "UTI": "120",
    "SMP": "121",
    "SM": "122",
    "PTP": "123",
    "ISIS": "124",
    "FIRE": "125",
    "CRTP": "126",
    "CRUDP": "127",
    "SSCOPMCE": "128",
    "IPLT": "129",
    "SPS": "130",
    "PIPE": "131",
    "SCTP": "132",
    "FC": "133",
    "RSVP-E2E-IGNORE": "134",
    "MOBILITY-HEADER": "135",
    "UDPLITE": "136",
    "MPLS-in-IP": "137",
    "MANET": "138",
    "HIP": "139",
    "SHIM6": "140",
    "WESP": "141",
    "ROHC": "142",
}


def true_false_checker(value):
    if type(value) is str:
        value = value.lower()
        if value == "true":
            return True
        elif value == "false":
            return False
    elif type(value) is int:
        if value == 1:
            logging.warning(
                f"Value, {value}, should be True or False.  Assuming you meant True."
            )
            return True
        elif value == 0:
            logging.warning(
                f"Value, {value}, should be True or False.  Assuming you meant False."
            )
            return False
    elif type(value) is bool:
        return value

    logging.warning(f"Invalid value: '{value}'. Should be True or False")
    return value


def syntax_correcter(value, permitted_syntax="""[.\w\d_\-]""", replacer="_"):
    """
    Check 'value' for invalid characters (identified by 'permitted_syntax') and replace them with 'replacer'.

    :param value:  (str) String to be checked.
    :param permitted_syntax: (str) regex of allowed characters.
    :param replacer: (str) character used to replace invalid characters.
    :return: (str) Modified string with "updated" characters.
    """
    logging.debug("In syntax_correcter() helper_function.")
    new_value = ""
    for char in range(0, len(value)):
        if not re.match(permitted_syntax, value[char]):
            new_value += replacer
        else:
            new_value += value[char]
    return new_value


def get_networkaddress_type(value):
    """
    Check to see whether 'value' is a host, range, or network.

    :param value: (str) x.x.x.x, x.x.x.x/xx, or x.x.x.x-x.x.x.x
    :return: (str) 'host', 'network', or 'range'
    """
    logging.debug("In get_networkaddress_type() helper_function.")
    if "/" in value:
        ip, bitmask = value.split("/")
        if bitmask == "32" or bitmask == "128":
            return "host"
        else:
            return "network"
    else:
        if "-" in value:
            return "range"
        else:
            return "host"


def is_ip(ip):
    """
    Check whether the provided string is an IP address.

    :param ip: (str) x.x.x.x
    :return: (boolean)
    """
    logging.debug("In is_ip() helper_function.")
    try:
        ipaddress.ip_address(ip)
    except ValueError as err:
        logging.error(err)
        return False
    return True


def is_ip_network(ip):
    """
    Check whether provided string is a valid network address.

    See if the provided IP/SM is the "network address" of the subnet.

    :param ip: (str) x.x.x.x/xx
    :return: (boolean)
    """
    logging.debug("In is_ip_network() helper_function.")
    try:
        ipaddress.ip_network(ip)
    except ValueError as err:
        logging.error(err)
        return False
    return True


def validate_ip_bitmask_range(value="", value_type=""):
    """
    We need to check the provided IP address (or range of addresses) and make sure the IPs are valid.

    :param value: (str) x.x.x.x, x.x.x.x/xx, or x.x.x.x-x.x.x.x
    :param value_type: (str) 'host', 'network', or 'range'
    :return: (dict) {value=value_fixed, valid=boolean}
    """
    logging.debug("In validate_ip_bitmask_range() helper_function.")
    return_dict = {"value": value, "valid": False}
    if value_type == "range":
        for ip in value.split("-"):
            if is_ip(ip):
                return_dict["valid"] = True
    elif value_type == "host" or value_type == "network":
        if is_ip_network(value):
            return_dict["valid"] = True
    return return_dict["valid"]


def mocked_requests_get(**kwargs):
    """
    Use to "mock up" a response from using the "requests" library to avoid actually using the "requests" library.

    :param kwargs:
    :return: (boolean)
    """
    logging.debug("In mocked_requests_get() helper_function.")

    class MockResponse:
        def __init__(self, **kwargs):
            logging.debug("In MockResponse __init__ method.")
            self.text = json.dumps(kwargs["text"])
            self.status_code = kwargs["status_code"]

        def close(self):
            logging.debug("In MockResponse close method.")
            return True

    return MockResponse(**kwargs)


def validate_vlans(start_vlan, end_vlan=""):
    """
    Validate that the start_vlan and end_vlan numbers are in 1 - 4094 range.  If not, then return 1, 4094.

    :param start_vlan: (int) Lower VLAN number in range.
    :param end_vlan: (int) Upper VLAN number in range.
    :return: (int) start_vlan, (int) end_vlan)
    """
    logging.debug("In validate_vlans() helper_function.")
    if end_vlan == "":
        end_vlan = start_vlan
    if int(end_vlan) < int(start_vlan):
        start_vlan, end_vlan = end_vlan, start_vlan
    if 0 < int(start_vlan) < 4095 and 0 < int(end_vlan) < 4095:
        return start_vlan, end_vlan
    else:
        return 1, 4094


def bulk_list_splitter(ids, chunk_size=49):
    """_summary_

    Args:
        ids (list): list of ids used in bulk post/delete operations
        chunk_size (int, optional): bulk operations seem to be limited to 49 max ids in one url. Defaults to 49.

    Returns:
        list: list of lists where each inner list is 49 items
    """
    chunks = []
    for id in range(0, len(ids), chunk_size):
        chunks.append(ids[id : id + chunk_size])
    return chunks


def check_uuid(uuid_input):
    try:
        uuid.UUID(str(uuid_input))
        return True
    except ValueError:
        return False


def get_protocol_number(protocol_name):
    """
    Map protocol name to IANA protocol number.

    :param protocol_name: (str) Protocol name ('TCP', 'UDP', 'ICMP', etc.)
    :return: (str) IANA protocol number
    """
    logging.debug("In get_protocol_number() helper_function.")
    protocol_number = PROTOCOL_MAP.get(protocol_name.upper())
    if protocol_number is None:
        raise ValueError(f"Unknown protocol: {protocol_name}")
    return protocol_number


def validate_port_literal(port, protocol="TCP"):
    """
    Validate and format a port literal for use in Access Rules.

    :param port: (str or int) Port number or port range (e.g., '80', '80-443')
    :param protocol: (str) Protocol name ('TCP', 'UDP', etc.)
    :return: (dict) Formatted port literal {'type': 'PortLiteral', 'port': '...', 'protocol': '...'}
    """
    logging.debug("In validate_port_literal() helper_function.")
    protocol_num = get_protocol_number(protocol)

    port = str(port)
    if "-" in port:
        parts = port.split("-")
        if len(parts) != 2:
            raise ValueError(f"Invalid port range: {port}")
        try:
            start_port = int(parts[0])
            end_port = int(parts[1])
        except ValueError:
            raise ValueError(f"Port range contains non-numeric values: {port}")
        if not (0 <= start_port <= 65535) or not (0 <= end_port <= 65535):
            raise ValueError(f"Port number out of valid range (0-65535): {port}")
        if start_port > end_port:
            raise ValueError(f"Invalid port range: start port ({start_port}) > end port ({end_port})")
    else:
        try:
            port_num = int(port)
        except ValueError:
            raise ValueError(f"Port must be numeric or a range: {port}")
        if not (0 <= port_num <= 65535):
            raise ValueError(f"Port number out of valid range (0-65535): {port}")

    return {"type": "PortLiteral", "port": port, "protocol": protocol_num}
