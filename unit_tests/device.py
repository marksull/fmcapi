import logging
import fmcapi
import time
import pprint
pp = pprint.PrettyPrinter(indent=4)


def test__device(fmc):
    logging.info('# Test Device.  Though you can "Post" devices I do not have one handy. So '
                 'add/remove licenses on Device Objects.')

    starttime = str(int(time.time()))
    namer = f'_fmcapi_test_{starttime}'

    acp1 = fmcapi.AccessControlPolicy(fmc=fmc, name=namer)
    acp1.post()
    obj1 = fmcapi.Device(fmc=fmc)
    obj1.name = namer
    obj1.acp(name=acp1.name)
    obj1.licensing(action='add', name='MALWARE')
    obj1.licensing(action='add', name='VPN')
    obj1.licensing(action='remove', name='VPN')
    obj1.licensing(action='clear')
    obj1.licensing(action='add', name='BASE')
    print('Device -->')
    pp.pprint(obj1.format_data())
    print('\n')
    acp1.delete()
    logging.info('# Test Device done.\n')
