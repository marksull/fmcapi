"""
All Audit Services features are in the FMC class in the fmc.py file.
"""

import logging
from .audit_records import AuditRecords

logging.debug("In the audit_services __init__.py file.")

__all__ = ["AuditRecords"]
