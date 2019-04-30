#!/usr/bin/python

import sys
import re
import csv
import traceback
import screener

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 8 :
   print "usage: " + program_name + " <debug_level : 1-4> <screener-data.csv> ... "
   sys.exit(1) 

debug_level = int(sys.argv[1])
isin_bse_filename = sys.argv[2]
isin_nse_filename = sys.argv[3]
in_amfi_filename = sys.argv[4]
sc_aliases_filename = sys.argv[5]
sc_data_1_filename = sys.argv[6]
sc_data_2_filename = sys.argv[7]
out_filename_phase1 = sys.argv[8]
out_filename_phase2 = sys.argv[9]
	
if debug_level > 1 :
	print 'args :' , len(sys.argv)

screener = screener.Screener()

screener.set_debug_level(debug_level)

screener.load_isin_data_both(isin_bse_filename, isin_nse_filename)
screener.load_amfi_data(in_amfi_filename)

screener.load_screener_name_aliases(sc_aliases_filename)
screener.load_screener_data(sc_data_1_filename)
screener.load_screener_data(sc_data_2_filename)

screener.print_phase1(out_filename_phase1)
screener.print_phase2(out_filename_phase2)
