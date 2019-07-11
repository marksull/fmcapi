# Example topology with scripts
The point of this example is to configure the following topology exclusively via the fmcapi project.
![](fmcapi_example_network.png)

## Prerequisites
The fmcapi talks to FMC and not the FTD/NGIPS devices directly so you will need to configure those devices to register 
to the FMC some other way (maybe the Ansible FTD modules?).

## FTD at HQ
We need to configure the FTD device at HQ prior to doing the branches because it is inline between the FMC and those 
branch devices.

Using the hq-ftd.py script we will accomplish the following:
* Create ACP (for HQ location).
* Add the hq-ftd device to the FMC.
* 
