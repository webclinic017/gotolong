#!/usr/bin/python

import sys
import re
import csv
import traceback
import isin

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 4 :
   print "usage: " + program_name + " <debug_level : 1-4> <isin.csv> ... "
   sys.exit(1) 

debug_level = int(sys.argv[1])
bse_filename = sys.argv[2]
nse_filename = sys.argv[3]
out_filename = sys.argv[4]
	
if debug_level > 1 :
	print 'args :' , len(sys.argv)

isin = isin.Isin()

isin.set_debug_level(debug_level)

isin.load_isin_data(bse_filename, 'bse')
isin.load_isin_data(nse_filename, 'nse')

isin.print_phase1(out_filename)
