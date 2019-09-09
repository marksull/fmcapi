import logging
import fmcapi
import pprint
pp = pprint.PrettyPrinter(indent=4)


def test__static_routes(fmc):
    logging.info('# Testing StaticRoutes class. Requires a registered device')

    obj1 = fmcapi.StaticRoutes(fmc=fmc)
    obj1.device(device_name="device_name")
    print('All StaticRoutes -- >')
    result = obj1.get()
    pp.pprint(result)
    print(f"Total items: {len(result['items'])}")
    print('\n')
    del obj1

    logging.info('# Testing StaticRoutes class done.\n')
