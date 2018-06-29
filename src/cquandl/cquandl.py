#!/usr/bin/python

import quandl
import os

quandl.ApiConfig.api_key = open(os.environ.get('HOME') + '/quandl.key', 'r').read().rstrip()

# quandl.get("NSE/RELIANCE", collapse="quarterly", start_date="1998-03-19")
mydata = quandl.get("NSE/RELIANCE", collapse="annual", start_date="1998-03-19")

print mydata
