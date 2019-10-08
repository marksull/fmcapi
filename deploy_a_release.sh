#!/bin/bash

echo "Building a new release of fmcapi!"
echo
echo "Did you remember to run black???"
echo

echo "Clean up old build"
rm -Rf build
rm -Rf dist
rm -Rf fmcapi.egg-info

echo "Make a new build"
python3 setup.py bdist_wheel
python3 setup.py sdist
twine upload dist/*
