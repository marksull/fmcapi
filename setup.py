from setuptools import setup, find_packages

__author__ = "Dax Mickelson"
__author_email = "dmickels@cisco.com"
__license__ = "BSD"

setup(
    name="fmcapi",
    version="20220914.0",
    description="Easier interface to Cisco's FMC API than writing your own way.",
    long_description="""With the removal to configure a Cisco NGFW via the command line your only option is to
     do so via a manager.  Some things are better when automated so using the manager's API gives us that power. 
     However, the current way to write external scripts and interact with the FMC's API isn't that great.  We created 
     this "wrapper" to give you an easier to use way of communicating with the FMC's API than using the example code 
     provided in the API Explorer.""",
    url="https://github.com/daxm/fmcapi",
    author="Dax Mickelson",
    author_email="dmickels@cisco.com",
    license="BSD",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking :: Firewalls",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    keywords="fmcapi fmc ftd security cisco ngfw api firepower",
    packages=find_packages(exclude=["docs", "tests*"]),
    install_requires=["requests", "datetime", "ipaddress"],
    python_requires=">=3.6",
    package_data={},
    data_files=None,
)
