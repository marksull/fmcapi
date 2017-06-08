"""
The fmcapi __init__.py file is called whenever someone imports the package into their program.
"""

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

# Its always good to set up a log file.
logging_format = '%(asctime)s - %(levelname)s:%(filename)s:%(lineno)s - %(message)s'
logging_dateformat = '%Y/%m/%d-%H:%M:%S'
# Logging level options are logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
logging_level = logging.INFO
#logging_level = logging.DEBUG
logging_filename = 'output.log'
logging.basicConfig(format=logging_format, datefmt=logging_dateformat, filename=logging_filename, level=logging_level)

"""
When someone "imports *" from a package the __all__ list is what is imported.
Thanks to David Beazley's (Live and Let Die!) youtube video I'm configuring this variable to only
expose those functions and/or classes I want using the @export decorator.
"""
__all__ = []

# A decorator to add functions and/or classes to the __all__ list.
def export(defn):
    globals()[defn.__name__] = defn
    __all__.append(defn.__name__)
    return defn

from . import fmc

logging.debug("In the fmcapi __init__.py file.")


def __authorship__():
        """In the FMC __authorship__() class method:
***********************************************************************************************************************
This python module was created by Dax Mickelson along with LOTs of help from Ryan Malloy and Neil Patel.
Feel free to send me comments/suggestions/improvements.  Either by email: dmickels@cisco.com or more importantly
via a Pull request from the github repository: https://github.com/daxm/fmcapi.
***********************************************************************************************************************
        """
        logging.debug(__authorship__.__doc__)
__authorship__()
