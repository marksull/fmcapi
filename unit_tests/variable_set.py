import logging
import fmcapi
import pprint
pp = pprint.PrettyPrinter(indent=4)


def test__variable_set(fmc):
    logging.info('Test VariableSet. Can only GET VariableSet objects.')

    obj1 = fmcapi.VariableSet(fmc=fmc)
    obj1.get(name='Default-Set')
    print('VariableSet -->')
    pp.pprint(obj1.format_data())
    print('\n')

    logging.info('# Test VariableSet done.\n')
