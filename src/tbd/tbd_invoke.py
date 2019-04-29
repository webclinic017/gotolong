#!/usr/bin/python

import sys
import re
import csv
import traceback
import tbd 

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 15 :
   print "usage: " + program_name + " <debug_level : 1-4> <isin-bse.csv> <isin-nse.csv> <amfi.csv> <plan.csv> <demat.csv>... "
   sys.exit(1) 

debug_level = int(sys.argv[1])
isin_bse_filename = sys.argv[2]
isin_nse_filename = sys.argv[3]
amfi_filename = sys.argv[4]
screener_aliases_filename = sys.argv[5]
plan_filename = sys.argv[6]
demat_filename = sys.argv[7]
screener_filename = sys.argv[8]

out_filename_phase1 = sys.argv[9]
out_filename_phase2 = sys.argv[10]
out_filename_phase3 = sys.argv[11]
out_filename_phase4 = sys.argv[12]
out_filename_phase5 = sys.argv[13]
out_filename_phase6 = sys.argv[14]
filter_days_1 = int(sys.argv[15])
filter_days_2 = int(sys.argv[16])
	
if debug_level > 1 :
	print 'args :' , len(sys.argv)

tbd = tbd.Tbd()

tbd.set_debug_level(debug_level)
tbd.load_tbd_data(isin_bse_filename, isin_nse_filename, amfi_filename, screener_aliases_filename, plan_filename, demat_filename, screener_filename)

tbd.print_tbd_phase1(out_filename_phase1)
tbd.print_tbd_phase2(out_filename_phase2)
tbd.print_tbd_phase3(out_filename_phase3)
tbd.print_tbd_phase4(out_filename_phase4, filter_days_1)
tbd.print_tbd_phase5(out_filename_phase5, filter_days_2)
tbd.print_tbd_phase6(out_filename_phase6)
