FROM python:3
MAINTAINER Dax Mickelson (dmickels@cisco.com)

WORKDIR /usr/src/app

ENV python_script TestingUserScript.py

RUN pip install --no-cache-dir fmcapi

CMD python $python_script
