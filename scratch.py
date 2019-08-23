from fmcapi.fmc import *
from fmcapi.api_objects.helper_functions import *
import json

# ### Set these variables to match your environment. ### #

host = 'fmclab.tor.afilias-int.info'
username = 'apiadmin'
password = 'LetsTalkAPI'
autodeploy = False


class PyJSON(object):
    def __init__(self, d):
        if type(d) is str:
            d = json.loads(d)
        self.from_dict(d)

    def from_dict(self, d):
        self.__dict__ = {}
        for key, value in d.items():
            if type(value) is dict:
                value = PyJSON(value)
            self.__dict__[key] = value

    def to_dict(self):
        d = {}
        for key, value in self.__dict__.items():
            if type(value) is PyJSON:
                value = value.to_dict()
            d[key] = value
        return d

    def __repr__(self):
        return str(self.to_dict())

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]


def get_nat(fmc, policy_name):
    '''
    Seems to return only AutoNat Rules
    '''
    result = NatRules(fmc)
    for policy in policy_name:
        print('Printing NAT rules for policy: {}'.format(policy.upper()))
        logging.debug('Printing NAT rules for policy: {}'.format(policy))
        result.nat_policy(policy)
        nat_rules = result.get()
        #pp.pprint(nat_rules)
        #[print(PyJSON(element).destinationInterface.name, PyJSON(element).natType, PyJSON(element).originalNetwork.name) for element in nat_rules['items']]

        return nat_rules


def get_nat_policy_names(fmc):
    policy = FTDNatPolicy(fmc)
    result = [PyJSON(policy_nat_dict).name for policy_nat_dict in policy.get()['items']]
    #print('Function get_nat_policy_names returns: {}'. format(result))
    return result


with FMC(host=host, username=username, password=password, autodeploy=autodeploy) as fmc1:

    nat_policy_names = get_nat_policy_names(fmc1)
    k = get_nat(fmc1, nat_policy_names)

if 'items' in k:
    for e in (map(lambda x : PyJSON(x),k['items'])):
        if e.metadata.section == 'AUTO':
            print(e.sourceInterface.name, e.originalNetwork.name, e.destinationInterface.name, e.translatedNetwork.name)
        if e.metadata.section == 'BEFORE_AUTO':
            print(e.sourceInterface.name, e.destinationInterface.name, e.originalSource.name, e.translatedSource.name)






