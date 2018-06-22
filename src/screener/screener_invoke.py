#!/usr/bin/python

import sys
import re
import csv
import traceback
import screener

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 4 :
   print "usage: " + program_name + " <debug_level : 1-4> <screener-data.csv> ... "
   sys.exit(1) 

debug_level = int(sys.argv[1])
in_filename = sys.argv[2]
out_filename = sys.argv[3]
	
if debug_level > 1 :
	print 'args :' , len(sys.argv)

screener = screener.Screener()

screener.set_debug_level(debug_level)

screener.load_screener_data(in_filename)

screener.print_phase1(out_filename)
