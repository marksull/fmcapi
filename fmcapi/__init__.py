"""
The fmcapi __init__.py file is called whenever someone imports the package into their program.
"""

# from .fmc import *
# from .api_objects import *
# from .helper_functions import *
import logging
logging.debug("In the fmcapi __init__.py file.")


def __authorship__():
    """In the FMC __authorship__() class method:
***********************************************************************************************************************
This python module was created by Dax Mickelson along with LOTs of help from Ryan Malloy and Neil Patel.  Thank you to
the github community members who have also pitched in, especially Mark Sullivan and his team.
Feel free to send me comments/suggestions/improvements.  Either by email: dmickels@cisco.com or more importantly
via a Pull request from the github repository: https://github.com/daxm/fmcapi.
***********************************************************************************************************************
        """
    logging.debug(__authorship__.__doc__)


__authorship__()
