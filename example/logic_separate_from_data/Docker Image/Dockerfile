FROM python:3
MAINTAINER Dax Mickelson (dmickels@cisco.com)

WORKDIR /usr/src/app

ENV python_script program_logic.py
ENV userdata userdata.yml

COPY ./requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

#CMD ["python", $python_script, "-d", $userdata]
CMD python $python_script -d $userdata
