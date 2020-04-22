#!/bin/bash

rm -Rf dist
python setup.py sdist
twine upload dist/*

