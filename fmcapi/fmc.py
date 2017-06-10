"""
This module (fmc.py) is designed to provide a "toolbox" of tools for interacting with the Cisco FMC API.
The "toolbox" is the FMC class and the "tools" are its methods.

Note: There exists a "Quick Start Guide" for the Cisco FMC API too.  Just Google for it as it gets updated with each
 release of code.
"""

import logging
import datetime
import json
import requests
import time

import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from .helper_functions import *
from .api_objects import *
from . import export

# Disable annoying HTTP warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Print the DOCSTRING for this module.
logging.debug(__doc__)

""""
The 'requests' package is very chatty on the INFO logging level.  Change its logging threshold sent to logger to 
something greater than INFO (i.e. not INFO or DEBUG) will cause it to not log its INFO and DEBUG messages to the 
default logger.  This reduces the size of our log files.
"""
logging.getLogger("requests").setLevel(logging.WARNING)


@export
class FMC(object):
    """
The FMC class has a series of methods, lines that start with "def", that are used to interact with the Cisco FMC
via its API.  Each method has its own DOCSTRING (like this triple quoted text here) describing its functionality.
    """
    logging.debug("In the FMC() class.")

    API_CONFIG_VERSION = 'api/fmc_config/v1'
    VERIFY_CERT = False

    def __init__(self, host='192.168.45.45', username='admin', password='Admin123', autodeploy=True):
        """
        Instantiate some variables prior to calling the __enter__() method.
        :param host:
        :param username:
        :param password:
        :param autodeploy:
        """
        logging.debug("In the FMC __init__() class method.")

        self.host = host
        self.username = username
        self.password = password
        self.autodeploy = autodeploy

    def __enter__(self):
        """
        Get a token from the FMC as well as the Global UUID.  With this information set up the base_url variable.
        :return:
        """
        logging.debug("In the FMC __enter__() class method.")
        self.mytoken = Token(host=self.host, username=self.username, password=self.password, verify_cert=self.VERIFY_CERT)
        self.uuid = self.mytoken.uuid
        self.base_url = "https://{}/{}/domain/{}".format(self.host, self.API_CONFIG_VERSION, self.uuid)
        return self

    def __exit__(self, *args):
        """
        If autodeploy == True push changes to FMC upon exit of "with" contract.
        :param args:
        :return:
        """
        logging.debug("In the FMC __exit__() class method.")

        if self.autodeploy:
            self.deploy_changes()
        else:
            logging.info("Auto deploy changes set to False.  "
                         "Use the Deploy button in FMC to push changes to FTDs.\n\n")

    def send_to_api(self, method='', url='', json_data=None):
        """
        Using the "method" type, send a request to the "url" with the "json_data" as the payload.
        :param method:
        :param url:
        :param json_data:
        :return:
        """
        logging.debug("In the FMC send_to_api() class method.")

        headers = {'Content-Type': 'application/json', 'X-auth-access-token': self.mytoken.get_token()}
        url = self.base_url + url
        status_code = 429
        response = None
        json_response = None
        try:
            while status_code == 429:
                if method == 'get':
                    response = requests.get(url, headers=headers, verify=self.VERIFY_CERT)
                elif method == 'post':
                    response = requests.post(url, json=json_data, headers=headers, verify=self.VERIFY_CERT)
                elif method == 'put':
                    response = requests.put(url, json=json_data, headers=headers, verify=self.VERIFY_CERT)
                elif method == 'delete':
                    response = requests.delete(url, headers=headers, verify=self.VERIFY_CERT)
                else:
                    logging.error("No request method given.  Returning nothing.")
                    return
                status_code = response.status_code
                if status_code == 429:
                    logging.warning("Too many connections to the FMC.  Waiting 30 seconds and trying again.")
                    time.sleep(30)
            json_response = json.loads(response.text)
            if status_code > 301 or 'error' in json_response:
                response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.error("Error in POST operation --> {}".format(str(err)))
            logging.error("json_response -->\t{}".format(json_response))
        if response:
            response.close()
        return json_response

    def get_deployable_devices(self):
        """
        Collect a list of FMC managed devices who's configuration is not up-to-date.
        :return: List of devices needing updates.
        """
        logging.debug("In the FMC get_deployable_devices() class method.")

        waittime = 15
        logging.info("Waiting {} seconds to allow the FMC to update the list of deployable devices.".format(waittime))
        time.sleep(waittime)
        logging.info("Getting a list of deployable devices.")
        url = "/deployment/deployabledevices?expanded=true"
        response = self.send_to_api(method='get', url=url)
        # Now to parse the response list to get the UUIDs of each device.
        if 'items' not in response:
            return
        uuids = []
        for item in response['items']:
            if not item['canBeDeployed']:
                pass
            else:
                uuids.append(item['device']['id'])
        return uuids

    def deploy_changes(self):
        """
        Iterate through the list of devices needing deployed and submit a request to the FMC to deploy changes to them.
        :return:
        """
        logging.debug("In the deploy_changes() class method.")

        url = "/deployment/deploymentrequests"
        devices = self.get_deployable_devices()
        if not devices:
            logging.info("No devices need deployed.\n\n")
            return
        nowtime = int(1000000 * datetime.datetime.now().timestamp())
        json_data = {
            'type': 'DeploymentRequest',
            'forceDeploy': True,
            'ignoreWarning': True,
            'version': nowtime,
            'deviceList': []
        }
        for device in devices:
            logging.info("Adding device {} to deployment queue.".format(device))
            json_data['deviceList'].append(device)
        logging.info("Deploying changes to devices.")
        response = self.send_to_api(method='post', url=url, json_data=json_data)
        return response['deviceList']

    # These are the "old" ways to CRUD FMC Objects.

    def create_acp_rules(self, rules):
        """
        Create ACP Rule Objects.
        :param rules:
        :return:
        """
        logging.debug("In the FMC create_acp_rules() class method.")

        logging.info("Creating ACP Rules.")
        for rule in rules:
            # Get ACP's ID for this rule
            url_search = "/policy/accesspolicies" + "?name=" + rule['acpName']
            response = self.send_to_api(method='get', url=url_search)
            acp_id = None
            if response.get('items', '') is '':
                logging.error("\tAccess Control Policy not found. Exiting.")
                sys.exit(1)
            else:
                acp_id = response['items'][0]['id']
            # NOTE: This json_data is written specific to match what I'm setting from the acpRuleList.
            # It will need to be updated if/when I create more advanced ACP Rules.
            json_data = {
                'name': rule['name'],
                'action': rule['action'],
                'type': 'AccessRule',
                'enabled': rule['enabled'],
                'sendEventsToFMC': True,
                'logBegin': rule['logBegin'],
                'logEnd': rule['logEnd'],
            }
            if rule.get('ipsPolicy', '') is not '':
                # Currently you cannot query IPS Policies by name.  I'll have to grab them all and filter from there.
                url_search = "/policy/intrusionpolicies"
                response = self.send_to_api(method='get', url=url_search)
                ips_policy_id = None
                for policie in response['items']:
                    if policie['name'] == rule['ipsPolicy']:
                        ips_policy_id = policie['id']
                if ips_policy_id is None:
                    logging.warning("\tIntrusion Policy {} is not found.  Skipping ipsPolicy "
                                    "assignment.\n\t\tResponse:{}".format(policie['name'], response))
                else:
                    json_data['ipsPolicy'] = {
                        'name': rule['ipsPolicy'],
                        'id': ips_policy_id,
                        'type': 'IntrusionPolicy'
                    }
            if rule.get('sourceZones', '') is not '':
                # NOTE: There can be more than one sourceZone so we need to account for them all.
                securityzone_ids = []
                for zone in rule['sourceZones']:
                    url_search = "/object/securityzones" + "?name=" + zone['name']
                    response = self.send_to_api(method='get', url=url_search)
                    if response.get('items', '') is '':
                        logging.warning("\tSecurity Zone {} is not found.  Skipping destination zone "
                                        "assignment.\n\t\tResponse:{}".format(zone['name'], response))
                    else:
                        tmp = {
                            'name': zone['name'],
                            'id': response['items'][0]['id'],
                            'type': 'SecurityZone'
                        }
                        securityzone_ids.append(tmp)
                if len(securityzone_ids) > 0:
                    json_data['sourceZones'] = {
                        'objects': securityzone_ids
                    }
            if rule.get('destinationZones', '') is not '':
                # NOTE: There can be more than one destinationZone so we need to account for them all.
                securityzone_ids = []
                for zone in rule['destinationZones']:
                    url_search = "/object/securityzones" + "?name=" + zone['name']
                    response = self.send_to_api(method='get', url=url_search)
                    if response.get('items', '') is '':
                        logging.warning("\tSecurity Zone {} is not found.  Skipping destination zone "
                                        "assignment.\n\t\tResponse:{}".format(zone['name'], response))
                    else:
                        tmp = {
                            'name': zone['name'],
                            'id': response['items'][0]['id'],
                            'type': 'SecurityZone'
                        }
                        securityzone_ids.append(tmp)
                if len(securityzone_ids) > 0:
                    json_data['destinationZones'] = {
                        'objects': securityzone_ids
                    }
            if rule.get('sourceNetworks', '') is not '':
                # Currently you cannot query Network Objects by name.  I'll have to grab them all and filter from there.
                url_search = "/object/networkaddresses"
                # Grab a copy of the current Network Objects on the server and we will cycle through these for each
                # sourceNetwork.
                response_network_obj = self.send_to_api(method='get', url=url_search)
                network_obj_ids = []
                for network in rule['sourceNetworks']:
                    for obj in response_network_obj['items']:
                        if network['name'] == obj['name']:
                            tmp = {
                                'type': 'Network',
                                'name': obj['name'],
                                'id': obj['id']
                            }
                            network_obj_ids.append(tmp)
                if len(network_obj_ids) < 1:
                    logging.warning("\tNetwork {} is not found.  Skipping source network "
                                    "assignment.\n\t\tResponse:{}".format(rule['name'], response_network_obj))
                else:
                    json_data['sourceNetworks'] = {
                        'objects': network_obj_ids
                    }
            if rule.get('destinationNetworks', '') is not '':
                # Currently you cannot query Network Objects by name.  I'll have to grab them all and filter from there.
                url_search = "/object/networkaddresses"
                # Grab a copy of the current Network Objects on the server and we will cycle through these for each
                # sourceNetwork.
                response_network_obj = self.send_to_api(method='get', url=url_search)
                network_obj_ids = []
                for network in rule['destinationNetworks']:
                    for obj in response_network_obj['items']:
                        if network['name'] == obj['name']:
                            tmp = {
                                'type': 'Network',
                                'name': obj['name'],
                                'id': obj['id']
                            }
                            network_obj_ids.append(tmp)
                if len(network_obj_ids) < 1:
                    logging.warning("\tNetwork {} is not found.  Skipping destination network "
                                    "assignment.\n\t\tResponse:{}".format(rule['name'], response_network_obj))
                else:
                    json_data['destinationNetworks'] = {
                        'objects': network_obj_ids
                    }
            if rule.get('sourcePorts', '') is not '':
                # Currently you cannot query via by name.  I'll have to grab them all and filter from there.
                url_search = "/object/protocolportobjects"
                response_port_obj = self.send_to_api(method='get', url=url_search)
                port_obj_ids = []
                for port in rule['sourcePorts']:
                    for obj in response_port_obj['items']:
                        if port['name'] == obj['name']:
                            tmp = {
                                'type': 'ProtocolPortObject',
                                'name': obj['name'],
                                'id': obj['id'],
                            }
                            port_obj_ids.append(tmp)
                if len(port_obj_ids) < 1:
                    logging.warning("\tPort {} is not found.  Skipping source port "
                                    "assignment.\n\t\tResponse:{}".format(port['name'], response_port_obj))
                else:
                    json_data['sourcePorts'] = {
                        'objects': port_obj_ids
                    }
            if rule.get('destinationPorts', '') is not '':
                # Currently you cannot query via by name.  I'll have to grab them all and filter from there.
                url_search = "/object/protocolportobjects"
                response_port_obj = self.send_to_api(method='get', url=url_search)
                port_obj_ids = []
                for port in rule['destinationPorts']:
                    for obj in response_port_obj['items']:
                        if port['name'] == obj['name']:
                            tmp = {
                                'type': 'ProtocolPortObject',
                                'name': obj['name'],
                                'id': obj['id'],
                            }
                            port_obj_ids.append(tmp)
                if len(port_obj_ids) < 1:
                    logging.warning("\tPort {} is not found.  Skipping destination port "
                                    "assignment.\n\t\tResponse:{}".format(port['name'], response_port_obj))
                else:
                    json_data['destinationPorts'] = {
                        'objects': port_obj_ids
                    }
            # Update URL to be specific to this ACP's ruleset.
            url = "/policy/accesspolicies/" + acp_id + "/accessrules"
            response = self.send_to_api(method='post', url=url, json_data=json_data)
            if response.get('id', '') is not '':
                rule['id'] = response['id']
                logging.info("\tACP Rule {} created.".format(rule['name']))
            else:
                logging.error("Creation of ACP rule: {} failed to return an 'id' value.".format(rule['name']))

'''
    def register_devices(self, devices):
        """
        Register a device with the FMC.
        :param devices:
        :return:
        """
        logging.debug("In the FMC register_devices() class method.")

        logging.info("Registering FTD Devices.")
        for device in devices:
            json_data = {
                'type': 'Device',
                'name': device['name'],
                'hostName': device['hostName'],
                'regKey': device['regkey'],
                'version': device['version'],
                'license_caps': device['licenses'],
            }
            # Get ACP's ID for this rule
            url_search = "/policy/accesspolicies" + "?name=" + device['acpName']
            response = self.send_to_api(method='get', url=url_search)
            if response.get('items', '') is '':
                logging.error("\tAccess Control Policy not found. Exiting.")
                continue
            json_data['accessPolicy'] = {
                'name': device['acpName'],
                'id': response['items'][0]['id'],
                'type': 'AccessPolicy'
            }
            url = "/devices/devicerecords"
            response = self.send_to_api(method='post', url=url, json_data=json_data)
            if response.get('metadata', '') is not '':
                logging.info("\t%s registration can take some time (5 minutes or more)." % device['name'])
                logging.info("\t\tIssue the command 'show managers' on", device['name'], "to view progress.")

    def create_security_zones(self, zones):
        """
        Create Security Zones.
        :param zones:
        :return:
        """
        logging.debug("In the FMC create_security_zones() class method.")

        logging.info("Creating Security Zones.")
        url = "/object/securityzones"
        for zone in zones:
            json_data = {
                "type": "SecurityZone",
                "name": zone['name'],
                "description": zone['desc'],
                "interfaceMode": zone['mode'],
            }
            response = self.send_to_api(method='post', url=url, json_data=json_data)
            if response.get('id', '') is not '':
                zone['id'] = response['id']
                logging.info("\tCreated Security Zone {}.".format(zone['name']))
            else:
                logging.error("Creation of Security Zone: {} failed to return an 'id' value.".format(zone['name']))

    def modify_device_physical_interfaces(self, device_attributes):
        """
        This doesn't work yet.
        Modify an FTD device's interfaces.
        :param device_attributes:
        :return:
        """
        logging.debug("In the FMC modify_device_physical_interfaces() class method.")

        logging.info("Modifying Physical Interfaces on FTD Devices.")
        # Get ID of this FTD Device first.  Alas, you can't GET by name.  :-(
        url_search = "/devices/devicerecords"
        # Grab a copy of the current Devices on the server so that we can cycle through to find the one we want.
        response_devices = self.send_to_api(method='get', url=url_search)
        if response_devices.get('items', '') is '':
            # It there are no devices (or we can't query them for some reason) none of this will work.
            logging.info("\tQuery for a list of Devices failed.  Exiting.")
            return
        for attribute in device_attributes:
            # Find the Device ID for this set of interfaces.
            device_id = None
            for device in response_devices['items']:
                if device['name'] == attribute['deviceName']:
                    device_id = device['id']
            if device_id is None:
                logging.info("\tDevice {} is not found.  Skipping modifying "
                             "interfaces.".format(attribute['deviceName']))
            else:
                #  Now that we have the device's ID.  Time to loop through our physical interfaces and see if we can
                # match them to this device's interfaces to get an ID.
                for device in attribute['physicalInterfaces']:
                    url = url_search + "/" + device_id + "/physicalinterfaces"
                    url_search2 = url + "?name=" + device['name']
                    response_interface = self.send_to_api(method='get', url=url_search2)
                    if response_interface.get('items', '') is '':
                        logging.info("\tDevice {} has not physical interface "
                                     "named {}.".format(attribute['deviceName'], device['name']))
                    else:
                        # Get the ID for the Security Zone.
                        url_search3 = "/object/securityzones" + "?name=" + device['securityZone']
                        response_securityzone = self.send_to_api(method='get', url=url_search3)
                        if response_securityzone.get('items', '') is '':
                            logging.info("\tSecurity Zone {} is not found.  Skipping modifying interface {} for "
                                         "device {}.".format(device['securityZone'], device['name'],
                                                             attribute['deviceName']))
                        else:
                            # Time to modify this interface's information.
                            json_data = {
                                'type': 'PhysicalInterface',
                                'enabled': True,
                                'name': device['name'],
                                'id': response_interface['items'][0]['id'],
                                'ifname': device['ifName'],
                                'securityZone': {
                                    'id': response_securityzone['items'][0]['id'],
                                    'name': device['securityZone'],
                                    'type': 'SecurityZone'
                                },
                                'ipv4': device['ipv4'],
                            }
                    response = self.send_to_api(method='put', url=url, json_data=json_data)
                    if response.get('metadata', '') is not '':
                        logging.info("\tInterface {} on device {} has been modified.".format(device['name'],
                                                                                             attribute['deviceName']))
                    else:
                        logging.info("\tSomething wrong happened when modifying "
                                     "interface {} on device {}.".format(device['name'], attribute['deviceName']))

    def create_acps(self, policies):
        """
        Create Access Control Policy Objects.
        :param policies:
        :return:
        """
        logging.debug("In the FMC create_acps() class method.")

        logging.info("Creating Access Control Policies.")
        url = "/policy/accesspolicies"
        for policy in policies:
            json_data = {
                'type': "AccessPolicy",
                'name': policy['name'],
                'description': policy['desc'],
            }
            if False and policy.get('parent', '') is not '':
                # Modifying Metatdata is not supported so we cannot create "child" ACPs yet.  :-(
                url_search = url + "?name=" + policy['parent']
                response = self.send_to_api(method='get', url=url_search)
                json_data['metadata'] = {
                    'inherit': True,
                    'parentPolicy': {
                        'type': 'AccessPolicy',
                        'name': policy['parent'],
                        'id': response['items'][0]['id']
                    }
                }
            else:
                json_data['defaultAction'] = {'action': policy['defaultAction']}
            response = self.send_to_api(method='post', url=url, json_data=json_data)
            if response.get('id', '') is not '':
                policy['id'] = response['id']
                logging.info("\tCreated Access Control Policy {}.".format(policy['name']))
            else:
                logging.error("Creation of Access Control Policy: {} failed to return an "
                              "'id' value.".format(policy['name']))

    def create_protocol_port_objects(self, protocolports):
        """
        Create Port Objects.
        :param protocolports:
        :return:
        """
        logging.debug("In the FMC create_protocol_port_objects() class method.")

        logging.info("Creating Protocol Port Object.")
        url = "/object/protocolportobjects"
        for port in protocolports:
            json_data = {
                'name': port['name'],
                'port': port['port'],
                'protocol': port['protocol'],
                'type': 'ProtocolPortObject',
            }
            response = self.send_to_api(method='post', url=url, json_data=json_data)
            if response.get('id', '') is not '':
                port['id'] = response['id']
                logging.info("\tCreated port object: {}.".format(port['name']))
            else:
                logging.error("Creation of port object: {} failed to return an 'id' value.".format(port['name']))

    def create_urls(self, objects):
        """
        Create URL Objects.
        :param objects:
        :return:
        """
        logging.debug("In the FMC create_urls() class method.")

        logging.info("Creating URL Objects.")
        url = "/object/urls"
        for obj in objects:
            json_data = {
                'name': obj['name'],
                'url': obj['value'],
                'description': obj['desc'],
                'type': 'Url',
            }
            response = self.send_to_api(method='post', url=url, json_data=json_data)
            if response.get('id', '') is not '':
                obj['id'] = response['id']
                logging.info("\tCreated URL Object {}.".format(obj['name']))
            else:
                logging.error("Creation of URL Object: {} failed to return an 'id' value.".format(obj['name']))

    def create_network_objects(self, objects):
        """
        Create Network Objects.
        :param objects:
        :return:
        """
        logging.debug("In the FMC create_network_objects() class method.")

        logging.info("Creating Network Objects.")
        url = "/object/networks"
        for obj in objects:
            json_data = {
                'name': obj['name'],
                'value': obj['value'],
                'description': obj['desc'],
                'type': 'Network',
            }
            response = self.send_to_api(method='post', url=url, json_data=json_data)
            if response.get('id', '') is not '':
                obj['id'] = response['id']
                logging.info("\tCreated Network Object {}.".format(obj['name']))
            else:
                logging.error("Creation of Network Object: {} failed to return an 'id' value.".format(obj['name']))

   def create_host_objects(self, hosts):
        """
        Create a Host Object.
        :param hosts:
        :return:
        """
        logging.debug("In the FMC create_host_objects() class method.")

        logging.info("Creating Host Object.")
        url = "/object/hosts"
        for host in hosts:
            json_data = {
                'name': host['name'],
                'value': host['value'],
                'type': 'Host',
            }
            response = self.send_to_api(method='post', url=url, json_data=json_data)
            if response.get('id', '') is not '':
                host['id'] = response['id']
                logging.info("\tCreated host object: {}.".format(host['name']))
            else:
                logging.error("Creation of host object: {} failed to return an 'id' value.".format(host['name']))

 
'''


class Token(object):
    """
    The token is the validation object used with the FMC.

    """
    logging.debug("In the Token class.")

    MAX_REFRESHES = 3
    TOKEN_LIFETIME = 60 * 30
    API_PLATFORM_VERSION = 'api/fmc_platform/v1'

    def __init__(self, host='192.168.45.45', username='admin', password='Admin123', verify_cert=False):
        """
        Initialize variables used in the Token class.
        :param host:
        :param username:
        :param password:
        :param verify_cert:
        """
        logging.debug("In the Token __init__() class method.")

        self.__host = host
        self.__username = username
        self.__password = password
        self.verify_cert = verify_cert
        self.token_expiry = None
        self.token_refreshes = 0
        self.access_token = None
        self.uuid = None
        self.refresh_token = None
        self.generate_tokens()

    def generate_tokens(self):
        """
        Create new and refresh expired tokens.
        :return:
        """
        logging.debug("In the Token generate_tokens() class method.")

        if self.token_refreshes <= self.MAX_REFRESHES and self.access_token is not None:
            headers = {'Content-Type': 'application/json', 'X-auth-access-token': self.access_token,
                       'X-auth-refresh-token': self.refresh_token}
            url = 'https://{}/{}/auth/refreshtoken'.format(self.__host, self.API_PLATFORM_VERSION)
            logging.info("Refreshing tokens, {} out of {} refreshes, from {}.".format(self.token_refreshes,
                                                                                      self.MAX_REFRESHES, url))
            response = requests.post(url, headers=headers, verify=self.verify_cert)
            self.token_refreshes += 1
        else:
            headers = {'Content-Type': 'application/json'}
            url = 'https://{}/{}/auth/generatetoken'.format(self.__host, self.API_PLATFORM_VERSION)
            logging.info("Requesting new tokens from {}.".format(url))
            response = requests.post(url, headers=headers,
                                     auth=requests.auth.HTTPBasicAuth(self.__username, self.__password),
                                     verify=self.verify_cert)
            self.token_refreshes = 0
        self.access_token = response.headers.get('X-auth-access-token')
        self.refresh_token = response.headers.get('X-authrefresh-token')
        self.token_expiry = datetime.datetime.now() + datetime.timedelta(seconds=self.TOKEN_LIFETIME)
        self.uuid = response.headers.get('DOMAIN_UUID')

    def get_token(self):
        """
        Check validity of current token.  If needed make a new or resfresh.  Then return access_token.
        :return:
        """
        logging.debug("In the Token get_token() class method.")

        if datetime.datetime.now() > self.token_expiry:
            logging.info("Token Expired.")
            self.generate_tokens()
        return self.access_token
