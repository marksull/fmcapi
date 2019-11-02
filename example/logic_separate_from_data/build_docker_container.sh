#!/usr/bin/env bash

# Docker can only mount a file at instantiation and not during Build.
docker run --name=fmcapi -v ~/userdata.yml:./userdata.yml <name of source image>
