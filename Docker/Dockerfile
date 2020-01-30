FROM ubuntu:18.04
MAINTAINER Dax Mickelson (dmickels@cisco.com)

# Configure variables
ENV WORK_DIR /usr/src/app
WORKDIR $WORK_DIR
ENV PYTHON_SCRIPT bootstrap.py

# Running modernize/update the environment
RUN apt-get -y update
RUN apt-get install -y apt-utils
RUN apt-get -y dist-upgrade
RUN apt-get -y autoremove
RUN apt-get -y autoclean

# Install Python modules
RUN apt-get -y install python3 python3-pip

# Install Python modules needed for this script.
COPY requirements.txt $WORK_DIR
RUN python3 -m pip install --no-cache-dir -r $WORK_DIR/requirements.txt

# Copy over bootstrap file
COPY $PYTHON_SCRIPT $WORK_DIR

# Run script.
CMD python3 $WORK_DIR/$PYTHON_SCRIPT
