#!/bin/sh

sudo curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py 

# resolve requests error
# pip list | grep request

sudo -H pip install --ignore-installed requests==2.7.0

sudo -H pip install quandl

sudo -H pip install sklearn 
sudo -H pip install scipy

