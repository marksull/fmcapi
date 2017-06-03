from setuptools import setup, find_packages

__author__ = "Dax Mickelson"
__author_email = "dmickels@cisco.com"
__license__ = "BSD"

setup(
    name='fmcapi',
    version='0.1.0',
    description="Easier interface to Cisco's FMC API than writing your own way.",
    long_description="""With the removal to configure a Cisco NGFW via the command line your only option is to
     do so via a manager.  Some things are better when automated so using the manager's API gives us that power. 
     However, the current way to write external scripts and interact with the FMC's API isn't that great.  We created 
     this "wrapper" to give you an easier to use way of communicating with the FMC's API than using the example code 
     provided in the API Explorer.""",
    url='https://github.com/daxm/fmcapi',
    author=__author__,
    author_email=__author_email,
    license=__license__,
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Cisco Security Engineers',
        'Intended Audience :: Edcuation',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Natrual Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Security',
        'Topic :: Security :: NGFW',
        'Topic :: Security :: FTD',
        'Topic :: Security :: Firewpower',
        'Topic :: Security :: FMC',
    ],
    keywords='fmcapi fmc ftd security cisco ngfw api',
    packages=find_packages(exclude=['docs', 'tests*'],
                           install_requires=['requests', 'logging', 'datetime', 'json', 'time', 're', 'ipaddress'],
                           package_data={},
                           data_files=None,)
)
