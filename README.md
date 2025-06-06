FMCAPI was originally developed by Dax Mickelson (dmickels@cisco.com). Dax has moved on to other projects but has kindly
transferred the ownership of this repo so that we can keep it current!


# fmcapi

Provide an "easier to use" way of interacting with the Cisco FMC's API.
There is a LOT that has yet to be done in order to make this project 
have "feature parity" with all that can be done with the FMC's API.
That said, what is here works!

The fmcapi is published to PyPI.  This means you can install it via pip 
(`pip3 install fmcapi`)

## Features
* Creation and maintenance of the connection with the FMC.  This basically is care and feeding of the token.
* Register devices with FMC.
* Deploy changes to FMC managed devices.
* Can access API REST methods for: 
  * Host Objects
  * Network Objects
  * Range Objects
  * Port Objects
  * ICMPv4/ICMPv6 Objects
  * Security Zones Objects
  * Interface Group Objects
  * URL Objects
  * FQDNS Objects
  * IKEv1/IKEv1 IPsec Proposal and Policy Objects
  * DNS Server Groups
  * Access Control Policy (ACP)
  * ACP Rules
  * VLAN Tags
  * Devices/Device Groups/Device HA
  * FTD Device Interfaces
  * IPv4/IPv6 Static Routes
  * NAT Policy
  * and many more!  (74 total by my last count.)
* There is a "dry_run" feature where you can issue a get(), put(), post(), or delete() method call and, where supported
you'll get output of what "would" have been sent to the FMC instead of actually issuing that method call.  This is good
for troubleshooting your scripts.
* There is a 'show_json' method available to all fmcapi Classes that will just output the formatted data that is know
in that instantiated class.

This is now an installable Python package via pip!  I'm heavily developing this code so you might want to issue the 
command `pip3 install -U fmcapi` to update your installed version.

## Quickstart on how to use this package
First install it with: `pip3 install fmcapi`
Then to use the code best start a "with" statement that creates an instance of the FMC class like this: 
`with fmcapi.FMC(host='192.168.11.15', username='admin', password='Admin123', autodeploy=False) as fmc:`  
Then either code away referencing the fmc variable to get to the internal methods of the FMC class **or** utilize 
the various class objects to ease your coding needs.

If you are using cdFMC, your api requests will need to proxied to that cdFMC via CDO. The authentication mechanisms used here are different than on-prem FMC as it looks like CDO's webserver is proxying these api requests to "cloud" FMC. Thankfully, it seems like aside from authentication, cdFMC has all the same api endpoints available. Follow the instructions [here](https://www.cisco.com/c/en/us/td/docs/security/firepower/730/Rapid-Release/API/CDO/cloud_delivered_firewall_management_center_rest_api_quick_start_guide/Connecting_With_A_Client.html) to create a CDO user capable of using the CDO api. This process will give you a JWT token which is what will be used for authenticating to CDO api, even when sending api requests to the cdFMC api.

`with fmcapi.FMC(host='examplecompany.app.us.cdo.cisco.com', cdfmc=True, api_key=$JWT-TOKEN-FROM-CDO-API-USER autodeploy=False) as fmc:`

NOTE: This JWT token is NOT the token used when utilizing the cdFMC api-explorer. It looks like the authentication for the cdFMC api-explorer is handled under the hood by CDO authenticating the CDO user and then just using a embedded "api-explorer" user that is cisco managed. This probably also means that cdFMC api-explorer can only have one session since any CDO user that goes to the cdFMC api-explorer will just get a new session of the cdFMC user 'api-explorer' thus logging any other existing 'api-explorer' user out.
``

Building out an example network is in the "example" directory.  This isn't fully completed but it should help you get
an idea of what is possible.

I recorded a quick "howto" video which can be accessed via:  (This is outdated and I need to make new videos.) 
https://www.youtube.com/watch?v=4NIe3T-HjDw

## Using in the Docker container
There is a Docker image stored on DockerHub (dmickels/fmcapi) you can use to create Docker containers with.
The syntax is as follows: ```docker run -i --name fmcapi --rm --name fmcapi -v 'local directory with scripts':/usr/src/app dmickels/fmcapi:latest```

## Notes
* 1:  Check out the example directory's scripts for ideas on how to use fmcapi.
* 2:  A lot of work has gone into making fmcapi easier to use and to develop on.  Doing this has forced us to
issue a deprecation notice on some of the original fmcapi Classes (so that our Class names align with Cisco's
API call names).  **Take note of any deprecation warnings and move to the correct Class name in your scripts.**
* 3:  You can directly send requests to the FMC via the send_to_api() method in the FMC class.  This allows you 
to access any of the API features of the FMC.

## ToDos
* Write better how-to instructions.  (Anyone willing to help?) 
* Finish adding all the FMC API calls as fmcapi Classes.
