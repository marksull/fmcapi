# Mission Statement
The fmcapi is to an easy to use interface so that anyone interested in writing Python scripts to interact with the 
FMC's API can do so without needing to have deep knowledge of the proper JSON format nor the minimum required settings 
needed to issue valid requests to the API.

The fmcapi is to provide the following:
 * FMC connection setup/maintenance/teardown.  (AKA Authentication and token management.)
 * A "user friendly" mechanism for formatting JSON to send GET/POST/PUT/DELETE requests to the FMC's API.
 * A "user friendly" way of dealing with issues, such as minimum required fields, to perform API requests. 
 * Provide mechanisms for interacting with all API functions available in the FMC while also allowing more advanced 
 users the freedom of interacting more directly.  (AKA Don't lock out access to)

# Goals
  * Short term:
    * Create User Documentation.  Teach an end user how to use the fmcapi in their programs.
    * Fix bug(s)
    * Add PUT functionality to AccessControlPolicy class.  This will require the creation of a new class to deal with 
    DefaultAction(s).
    * Better error handling, especially around the cryptic response messages from the API.
  * Medium Term:
    * Add new API features as they are released.  (Such as NAT Policy/rule abilities, when they come available.)
    * Add feature(s) for Device Interface configuration.
    * Create Developer Documentation.  Help developers improve the fmcapi code.
    * Deal with "paging" in the responses from FMC.
  * Long Term:
    * Feature parity to all API features.
    * Version parity to allow for differences of available API features based on the version of FMC being used.
