First, thank you for taking a look around the code!

If you find something wrong, and you don't want to fix it, please open
an issue on github:  https://github.com/daxm/fmcapi/issues.

If you desire to write some code then please note these items:
*  Use the Cisco Quick Start Guide for FMC API to know where each API
class should be stored.  As you can see there are several sub-package
directories in the api_objects package.  Place your new Class file 
there.
* Please name the Python file and the Class you create to match the 
associated API method from the Quick Start Guide.  This will help users
know what is what.
* 99% of the time your Class should inherit from APIClassTemplate to get
all the additional Class methods.  No need for you to re-write that 
code!
* In both the api_objects'  dunder init and the sub-package's dunder 
init please import your specific Class and add it to the dunder all 
variable.
* Lastly, please create a "unit-test" for your new Class' features.
These unit-tests are referenced from the TestingUserScript.py file.

