from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.policy_services.prefilterpolicies import PreFilterPolicies
from fmcapi.api_objects.object_services.securityzones import SecurityZones
import logging


class PreFilterRules(APIClassTemplate):
    """
    The PreFilterRules object in the FMC
    """
    VALID_JSON_DATA = [
        "id",
        "name",
        "action"
    ]
    PREFIX_URL = '/policy/prefilterpolicies'
    VALID_FOR_ACTION = ['FASTPATH', 'ANALYZE', 'BLOCK']
    REQUIRED_FOR_POST = ['prefilter_id']
    REQUIRED_FOR_GET = ['prefilter_id']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for PreFilterRules class.")
        self.type = "PreFilterRules"
        self.prefilter_id = None
        self.prefilter_added_to_url = False
        self.action = 'FASTPATH'
        self.parse_kwargs(**kwargs)
        self.URL = f"{self.URL}{self.URL_SUFFIX}"

    @property
    def URL_SUFFIX(self):
        """
        Add the URL suffixes for insertBefore and insertAfter
        NOTE: You must specify these at the time of the object is initialized
        for this to work correctly. Example:
            This works:
                new_rule = PreFilterRules(fmc=fmc, prefilter_name='pre1', insertBefore=2)

            This does not:
                new_rule = PreFilterRules(fmc=fmc, prefilter_name='pre1')
                new_rule.insertBefore = 2
        """
        url = "?"
        if "insertBefore" in self.__dict__:
            url = f"{url}insertBefore={self.insertBefore}"
        elif "insertAfter" in self.__dict__:
            url = f"{url}insertAfter={self.insertAfter}"

        return url

    def parse_kwargs(self, **kwargs):
        """
        Parse the kwargs and load into object properties
        Args:
            kwargs (dict): Keyword arguments
        """
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for PreFilterRules class")

        if "prefilter_id" in kwargs:
            self.prefilter(prefilter_id=kwargs["prefilter_id"])
        if 'prefilter_name' in kwargs:
            self.prefilter(name=kwargs['prefilter_name'])
        if 'action' in kwargs:
            self.validate_action(kwargs['action'])

    def prefilter(self, name=None, prefilter_id=None):
        """
        If the name has been supplied, go and pull the prefilter ID. If ID has been specified, add it to self.
        Also create the URL for prefilter policy
        Args:
            name (str): Prefilter name
            prefilter_id (str): UUID of prefilter
        """
        logging.debug("In prefilter() for PreFilterRules")
        if not name and not prefilter_id:
            logging.warning(f'Unable to find prefilter as no name or ID was specified')

        elif name:
            logging.info(f'Searching ID for prefilter "{name}"')
            pre1 = PreFilterPolicies(fmc=self.fmc)
            pre1.get(name=name)

            if 'id' in pre1.__dict__:
                prefilter_id = pre1.id
            else:
                logging.warning(f'Prefilter policy {name} not found. Cannot setup perfilter policy for PreFilterRules')

        self.prefilter_id = prefilter_id
        self.URL = f'{self.fmc.configuration_url}{self.PREFIX_URL}/{self.prefilter_id}/prefilterrules'
        self.prefilter_added_to_url = True

    def validate_action(self, action):
        """
        Checks the provided action is valid and sets property
        Args:
            action (str): Prefilter rule action
        """
        if action in self.VALID_FOR_ACTION:
            self.action = action
        else:
            logging.warning(f'Action {action} is not a valid option\nValid actions are: {self.VALID_FOR_ACTION}')

    def source_zone(self, action, name=''):
        """
        Set the source zone information
        Args:
            action (str): "add" or "remove"
            name (str): Name of interface zone object
        """
        logging.debug('In source_zone() for PreFilterRules class.')
        if action == 'clear':
            if 'sourceZones' in self.__dict__:
                del self.sourceZones
                logging.info(f'Removed source zone from prefilter rule')

        elif action == 'add':
            src_zone_id, src_zone_type = self.get_zone_id(name)
            if src_zone_id:
                self.add_zone('sourceZones', name, src_zone_id, src_zone_type)
            else:
                logging.warning(f'Security zone object "{name}" not found on FMC')

    def destination_zone(self, action, name=''):
        """
        Set the destination zone information
        Args:
            action (str): "add" or "remove"
            name (str): Name of interface zone object
        """
        logging.debug('In source_zone() for PreFilterRules class.')
        if action == 'clear':
            if 'sourceZones' in self.__dict__:
                del self.destinationZones
                logging.info(f'Removed source zone from prefilter rule')

        elif action == 'add':
            dst_zone_id, dst_zone_type = self.get_zone_id(name)
            if dst_zone_id:
                self.add_zone('destinationZones', name, dst_zone_id, dst_zone_type)
            else:
                logging.warning(f'Security zone object "{name}" not found on FMC')

    def get_zone_id(self, name):
        """
        Pull the ID for a security zone
        Args:
            name (str): Name of interface zone object

        Returns:
            UUID of zone object (str)
        """
        sec_zone = SecurityZones(fmc=self.fmc)
        sec_zone.get(name=name)
        if 'id' in sec_zone.__dict__:
            return sec_zone.id, sec_zone.type
        else:
            return None, None

    def add_zone(self, target, name, id, zone_type):
        """
        Check if zone is already on object, skip if it is, add if it isn't and create sourceZone if that object
        attribute doesn't exist at all
        Args:
            target (str): "sourceZones" or "destinationZones"
            name (str): Name of zone object
            id (str): UUID of zone object
            zone_type (str): Security zone type
        """

        if target in self.__dict__:

            # Look through existing zones, if present, for the zone name. Skip if it's already there
            zone_name_duplicate = False
            zone_list = []
            for zone in getattr(self, target)['objects']:
                zone_list.append(zone)
                if zone['name'] == name:
                    zone_name_duplicate = True

            if not zone_name_duplicate:
                zone_list.append({'name': name, 'id': id, 'type': zone_type})
                setattr(self, target, {'objects': zone_list})

        # Set the zone if it doesn't exist
        else:
            setattr(self, target, {'objects': [{'name': name, 'id': id, 'type': zone_type}]})