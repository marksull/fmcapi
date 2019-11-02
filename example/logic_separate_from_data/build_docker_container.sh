#!/usr/bin/env bash

# Docker can only mount a file at instantiation and not during Build.
# "python_script" is the Python file that will be executed.
# "userdata" is the YAML data file to be sourced by python_script.
# "9b1974aae1fe" is the ID of the Docker image.  This will vary per each build of the image.  Use "docker images" to get the correct ID.
# the "-v" section should probably be left alone as it mounts the python_script and userdata defined values into the correct destination directory.
# --name gives the container a name (easier to use when needing to stop the container).
# --rm will remove the container once the script is done (or you stop the container).  This means you get a fresh container at each runtime.
docker run --name fmcapi --rm -e "python_script=program_logic.py" -e "userdata=userdata.yml" -v $(pwd):/usr/src/app 9b1974aae1fe
