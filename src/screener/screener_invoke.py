#!/usr/bin/python

import sys
import re
import csv
import traceback
import screener

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 7 :
   print "usage: " + program_name + " <debug_level : 1-4> <screener-data.csv> ... "
   sys.exit(1) 

debug_level = int(sys.argv[1])
isin_bse_filename = sys.argv[2]
isin_nse_filename = sys.argv[3]
sc_filename = sys.argv[4]
out_filename_phase1 = sys.argv[5]
out_filename_phase2 = sys.argv[6]
	
if debug_level > 1 :
	print 'args :' , len(sys.argv)

screener = screener.Screener()

screener.set_debug_level(debug_level)

screener.load_isin_data_both(isin_bse_filename, isin_nse_filename)
screener.load_screener_data(sc_filename)

screener.print_phase1(out_filename_phase1)
screener.print_phase2(out_filename_phase2)
