"""
Unit testing, of a sort, all the created methods/classes.
"""

from fmcapi.fmc import *
from fmcapi.api_objects import *
from fmcapi.helper_functions import *

# ### Set these variables to match your environment. ### #

host = '10.0.0.10'
username = 'apiadmin'
password = 'Admin123'
autodeploy = True


def main():
    with FMC(host=host, username=username, password=password, autodeploy=autodeploy) as fmc1:
        # Create ACP

        # Add hq-ftd device to FMC

        pass

if __name__ == "__main__":
    main()
