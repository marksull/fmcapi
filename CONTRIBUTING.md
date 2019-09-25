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
* In both the api_objects' `__init__.py` and the sub-package's `__init__.py` please import your specific Class and add it
 to the `__all__` variable.
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
* The various FMC API methods have differing rules on what is/isn't allowed in the 'name' field.  Please use the
VALID_CHARACTERS_FOR_NAME variable is to provide a regex "string" that describes what is permitted.  The real issue
here is whether spaces are/aren't permitted in the 'name'.
* When performing a GET, and not specifying an 'id', will generally render a list of all objects for that API method.
Some of these allow the ability to filter/search by name.  Use the FILTER_BY_NAME boolean variable to specify if this
is possible.
* If you copy/paste one Class to create a new one:  **PLEASE** carefully comb through the copied code and update it to be
accurate to your new Class.  Remove unneeded variables and class methods.  Update any logging/comments to match the
new Class.
* If specific variables are required for an FMC's API method please ensure your Class' REQUIRED_FOR_<method> variable
is set correctly.  (e.g. REQUIRED_FOR_GET = 'id')
* If you have a method in your Class that is used to add objects to a list (like a list of networks for a network group)
please use the following for the action variable (as applicable): 'add', 'remove', 'clear'.  This will provide a 
consistent "language" to the user's of fmcapi.
For example:
```
    def foo(self, action='', ...):
        if 'action' == 'add':
            blah
        elif 'action' == 'remove':
            blah
        elif 'action == 'clear':
            blah
```
* If you have a method in your Class that is used to add another class object (not a list like described above)
please use the following for the action variable (as applicable): 'set', 'clear'.  This will provide a  consistent 
"language" to the user's of fmcapi.
For example:
```
    def foo(self, action='', ...):
        if 'action' == 'set':
            blah
        elif 'action == 'clear':
            blah
```
