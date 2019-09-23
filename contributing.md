#Contributing Guidelines and Notes
First, thank you for taking a look around the code!

If you find something wrong, and you don't want to fix it, please open an issue on github:
https://github.com/daxm/fmcapi/issues.

##If you desire to write some code then please note these items:
* Use the Cisco Quick Start Guide for FMC API to know where each API class should be stored. As you can see there are 
several sub-package directories in the api_objects package. Place your new Class file there.  Please name the Python 
file and the Class you create to match the associated API method from the Quick Start Guide.  This will help users know 
what class is associated wot which FMC API method.
* 99% of the time your Class should inherit from APIClassTemplate to get all the additional Class methods. No need for 
you to re-write that code!
* In both the api_objects' dunder init and the sub-package's dunder init please import your specific Class and add it to
 the dunder all variable.
* Lastly, please create a "unit-test" for your new Class' features. These unit-tests are referenced from the 
TestingUserScript.py file.  Think of these "tests" as the best documentation that user's of the FMCAPI will have in
knowing how to use that particular Class.  (Unless you want to write up good use documentation too.)  :-)

##Misc Notes about adding code:
* You may not agree with me on this logic but I feel we need to control what is submitted to format_data() and/or 
parse_kwargs() class methods. It's been my experience that the FMC is VERY touchy about what is in the JSON payload so 
we might as well accept that we need to manage what is sent. So, you'll see that each API class has VALID_JSON_DATA and 
VALID_FOR_KWARGS variables. These are lists of variable names we will allow. Be sure to create/update these variables as
 you create/modify the Class(es).
* I know that the FMC API documentation is horrible for identifying which FMC version first released an API feature.
That said, please do your best to associate your Class to the correct version in which it was released.  This is what 
the FIRST_SUPPORTED_FMC_VERSION variable is for.
