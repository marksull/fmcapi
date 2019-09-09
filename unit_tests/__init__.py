import logging
from .url_category import test__url_category
from .ports import test__ports

logging.debug("In the unit-tests __init__.py file.")

__all__ = ['test__url_category',
           'test__ports',
           ]
