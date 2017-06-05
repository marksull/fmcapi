# fmcapi
Provide an "easier to use" way of interacting with the Cisco FMC's API.
There is a LOT that has yet to be done in order to make this project have "feature parity"
with all that can be done with the FMC's API.  That said, what is here works!

# Features
* Creation and maintenance of the connection with the FMC.  This basically is care and feeding
of the token.
* Register devices with FMC.
* Deploy changes to FMC managed devices.
* GET/POST/PUT/DELETE of:
  * Host Objects
  * Port Objects
  * Security Zones
  * Network Objects
  * URL Objects
  * Access Control Policy (ACP)
  * ACP Rules
* Expire "Dev" entries.  This is special for the Pinhole Self-Serve Tool lab.  (Should be
factored out to another project.)
* This is now an installable Python package via pip!  Currently v0.1.2.

# Quickstart on how to use this package
First install it with: **pip3 install fmcapi**
Then to use the code best start a "with" statement that creates an instance of the FMC class like this: **with FMC(host='192.168.11.15', username='admin', password='Admin123', autodeploy=False) as fmc:**
Then code away referencing the fmc variable to get to the internal methods of the FMC class.


# ToDos
* Move/Change the various "create" FMC class methods into the api_objects module.
* Build a complete system for all FMC API accessible objects (feature parity)