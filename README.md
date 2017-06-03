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

# ToDos
* Move/Change the various "create" FMC class methods into the api_objects module.
