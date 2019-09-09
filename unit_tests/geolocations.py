import logging
import fmcapi
import pprint
pp = pprint.PrettyPrinter(indent=4)


def test__geolocations(fmc):
    logging.info('Testing Geolocation class. Requires a configured Geolocation')

    obj1 = fmcapi.Geolocation(fmc=fmc)
    print('All Geolocation -- >')
    result = obj1.get()
    pp.pprint(result)
    print(f"Total items: {len(result['items'])}")
    print('\n')
    del obj1
    obj1 = fmcapi.Geolocation(fmc=fmc, name='_tmp')
    print('One Geolocation -- >')
    pp.pprint(obj1.get())
    print('\n')

    logging.info('# Testing Geolocation class done.\n')
