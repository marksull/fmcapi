from .monitoredinterfaces import MonitoredInterfaces


class DeviceHAMonitoredInterfaces(MonitoredInterfaces):
    """
    The DeviceHAMonitoredInterfaces Object in the FMC.
    This was the original class created but technically it is monitoredinterfaces in the API.
    So, this just inherits the "new" class to support legacy calls to this class.
    """
