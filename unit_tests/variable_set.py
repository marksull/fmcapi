import logging
import fmcapi


def test__variable_set(fmc):
    logging.info("Test VariableSet. Can only GET VariableSet objects.")

    obj1 = fmcapi.VariableSets(fmc=fmc)
    obj1.get(name="Default-Set")
    logging.info("VariableSet -->")
    logging.info(obj1.format_data())

    logging.info("Test VariableSet done.\n")
