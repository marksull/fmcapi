import logging
import fmcapi
import time
import json


def test__objects_get_query_filters(fmc):
    logging.info("Test Object Get Query Filters.  Get Objects that support their various get query filters.")

    #'_' in nameOrValue='_' is used as an example as we use underscores in our object names. 

    logging.info('Object: Networks')
    obj1 = fmcapi.Networks(fmc=fmc)
    obj1.get(nameOrValue='_')
    del obj1

    logging.info('Object: Hosts')
    obj1 = fmcapi.Hosts(fmc=fmc)
    obj1.get(nameOrValue='_')
    del obj1

    logging.info('Object: NetworkGroups')
    obj1 = fmcapi.NetworkGroups(fmc=fmc)
    groups = obj1.get(nameOrValue='_')
    print(json.dumps(groups, indent=2))
    del obj1

    logging.info('Object: Ports')
    obj1 = fmcapi.Ports(fmc=fmc)
    obj1.get(nameOrValue='_')
    del obj1

    logging.info('Object: ICMPv4Objects')
    obj1 = fmcapi.ICMPv4Objects(fmc=fmc)
    obj1.get(nameOrValue='_')
    del obj1

    logging.info('Object: ICMPv6Objects')
    obj1 = fmcapi.ICMPv6Objects(fmc=fmc)
    obj1.get(nameOrValue='_')
    del obj1

    logging.info('Object: ProtocolPortObjects')
    obj1 = fmcapi.ProtocolPortObjects(fmc=fmc)
    obj1.get(nameOrValue='_')
    del obj1

    logging.info('Object: PortObjectGroups')
    obj1 = fmcapi.PortObjectGroups(fmc=fmc)
    obj1.get(nameOrValue='_')
    del obj1

    logging.info('Object: VlanTags')
    obj1 = fmcapi.VlanTags(fmc=fmc)
    obj1.get(nameOrValue='_')
    del obj1

    logging.info('Object: VlanGroupTags')
    obj1 = fmcapi.VlanGroupTags(fmc=fmc)
    obj1.get(nameOrValue='_')
    del obj1

    logging.info('Object: URLs')
    obj1 = fmcapi.URLs(fmc=fmc)
    obj1.get(nameOrValue='_')
    del obj1

    logging.info('Object: URLGroups')
    obj1 = fmcapi.URLGroups(fmc=fmc)
    obj1.get(nameOrValue='_')
    del obj1

    logging.info('Object: NetworkAddresses')
    obj1 = fmcapi.NetworkAddresses(fmc=fmc)
    obj1.expanded = True
    addresses = obj1.get(nameOrValue='_')
    print(json.dumps(addresses, indent=2))
    del obj1

    logging.info('Object: Ranges')
    obj1 = fmcapi.Ranges(fmc=fmc)
    obj1.get(nameOrValue='_')
    del obj1

    logging.info('Object: FQDNs')
    obj1 = fmcapi.FQDNS(fmc=fmc)
    obj1.get(nameOrValue='_')
    del obj1

    logging.info('Object: AnyProtocolPortObjects')
    obj1 = fmcapi.AnyProtocolPortObjects(fmc=fmc)
    obj1.get(nameOrValue='_')
    del obj1

    logging.info("Test Object Get Query Filters done.\n")