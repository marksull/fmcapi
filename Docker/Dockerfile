FROM python:3.11.6-alpine3.18
MAINTAINER Dax Mickelson (dmickels@cisco.com)

# Configure variables
ENV WORK_DIR /usr/src/app
WORKDIR $WORK_DIR
ENV PYTHON_SCRIPT bootstrap.py

# Install Python modules needed for this script.
COPY requirements.txt $WORK_DIR
RUN python3 -m pip install --no-cache-dir -r $WORK_DIR/requirements.txt

# Copy over bootstrap file
COPY $PYTHON_SCRIPT $WORK_DIR

# Run script.
CMD python3 $WORK_DIR/$PYTHON_SCRIPT
