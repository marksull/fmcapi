#!/bin/bash

# Clean up old build
rm -Rf build
rm -Rf dist
rm -Rf fmcapi.egg-info

# Make a new build
python3 setup.py bdist_wheel
python3 setup.py sdist
twine upload dist/*