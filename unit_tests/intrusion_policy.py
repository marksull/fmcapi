import logging
import fmcapi
import pprint
pp = pprint.PrettyPrinter(indent=4)


def test__intrusion_policy(fmc):
    logging.info(
        '# Test IntrusionPolicy. Can only GET IntrusionPolicy objects.')
    obj1 = fmcapi.IntrusionPolicy(fmc=fmc)
    obj1.get(name='Security Over Connectivity')
    print('IntrusionPolicy -->')
    pp.pprint(obj1.format_data())
    print('\n')
    logging.info('# Test IntrusionPolicy done.\n')
