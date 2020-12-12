#!/usr/bin/env bash

# check value of WSGI_APPLICATION in mysite/settings.py
# WSGI_APPLICATION = 'mysite.wsgi.application'

# NOTE : It runs only on Linux ...
# Don't try it on windows
gunicorn --bind 0.0.0.0:8000 mysite.wsgi:application