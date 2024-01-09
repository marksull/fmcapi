import logging
import fmcapi


def test__dynamic_objects_mappings(fmc):
    logging.info("Testing Dynamic Objects Mappings")

    # obj1 = fmcapi.DynamicObjectMappings(fmc)
    # obj1.handle_mappings(action="add", value=["10.0.0.4"], name="Sales")
    # obj1.post()

    obj2 = fmcapi.DynamicObjectMappings(fmc=fmc, id="0050568E-B2F8-0ed3-0000-523986013212")
    #obj2.mappings = ["70.0.0.0/24"]
    logging.info(f"Dynamic object mapping {obj2.get()}")







