import logging
import fmcapi


def test__deployable_devices(fmc):
    """
    Test DeployableDevices() class with actual FMC connection.
    
    Tests:
    - Getting list of deployable devices
    - Getting pending changes for a specific device (if any deployable devices exist)
    - Verifying unsupported methods
    """
    logging.info("Testing DeployableDevices() class.")
    
    # Initialize and get list of deployable devices
    tmp = fmcapi.DeployableDevices(fmc=fmc)
    deployable_devices = tmp.get()
    
    if deployable_devices:
        logging.info(f"Found {len(deployable_devices)} deployable device(s):")
        for device in deployable_devices:
            logging.info(f"  - {device.get('name', 'Unknown')} (ID: {device.get('id', 'Unknown')})")
            
        # Test getting pending changes for the first deployable device
        first_device_id = deployable_devices[0].get('id')
        if first_device_id:
            logging.info(f"Getting pending changes for device: {first_device_id}")
            pending_changes = tmp.get(containerUUID=first_device_id)
            if pending_changes:
                logging.info("Pending changes retrieved successfully.")
            else:
                logging.info("No pending changes found for this device.")
    else:
        logging.info("No deployable devices found.")
    
    # Test unsupported methods
    logging.info("Testing unsupported methods (post, put, delete):")
    tmp.post()
    tmp.put()
    tmp.delete()
    
    logging.info("Testing DeployableDevices() method done.\n")
