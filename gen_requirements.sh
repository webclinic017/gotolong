#!/bin/sh

#generate requirements file
pip freeze | awk -F"==" '{print $1}' > requirements/requirements-dev.txt