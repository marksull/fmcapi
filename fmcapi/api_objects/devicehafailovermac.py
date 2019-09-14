from fmcapi.api_objects.device_ha_pair_services.failoverinterfacemacaddressconfigs import FailoverInterfaceMACAddressConfigs


class DeviceHAFailoverMAC(FailoverInterfaceMACAddressConfigs):
    """
    The DeviceHAFailoverMAC Object in the FMC.
    This was the original class created but technically it is failoverinterfacemacaddressconfigs in the API.
    So, this just inherits the "new" class to support legacy calls to this class.
    """
