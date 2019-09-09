import logging
from .url_category import test__url_category
from .ports import test__ports
from .upgrades import test__upgrades
from .manualnat import test__manualnat
from .autonat import test__autonat
from .protocolport import test__protocolport
from .audit import test__audit
from .acprule import test__acp_rule
from .acp import test__access_control_policy

logging.debug("In the unit-tests __init__.py file.")

__all__ = ['test__url_category',
           'test__ports',
           'test__upgrades',
           'test__manualnat',
           'test__autonat',
           'test__protocolport',
           'test__audit',
           'test__acp_rule',
           'test__access_control_policy',
           ]
