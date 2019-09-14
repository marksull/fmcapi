from .ftddevicehapairs import FTDDeviceHAPairs


class DeviceHAPairs(FTDDeviceHAPairs):
    """
    The DeviceHAPairs Object in the FMC.
    This was the original class created but technically it is FTD device HA pairs in the API.
    So, this just inherits the "new" FTDDeviceHAPairs class to support legacy calls to this class.
    """
