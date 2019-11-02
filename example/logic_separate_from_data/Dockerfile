FROM python:3
MAINTAINER Dax Mickelson (dmickels@cisco.com)

ENV userdata userdata.yml
ENV python_script program_logic.py

WORKDIR ./

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./$python_script", "-d", "$userdata"]
