"""
All Deployment Services features are in the FMC class in the fmc.py file.
"""

import logging
from .deployabledevices import DeployableDevices
from .deploymentrequests import DeploymentRequests

logging.debug("In the deployment_services __init__.py file.")

__all__ = ["DeployableDevices", "DeploymentRequests"]
