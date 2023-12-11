import logging
import fmcapi


def test__dynamic_objects(fmc):
    logging.info("Testing Dynamic Objects.")
    result = fmcapi.DynamicObject(fmc=fmc).get()
    logging.info(f"All Dynamic Objects ---> {result}")
    logging.info(f"Total items: {len(result['items'])}")

    obj1 = fmcapi.DynamicObject(fmc=fmc, name="Platform",
    description="IPs of Engineer department",
    type="DynamicObject", objectType="IP",).post()

    obj1 = fmcapi.DynamicObject(fmc=fmc, name="NWS")
    obj1.get()
    logging.info(f"One objectby name----> {obj1}")

