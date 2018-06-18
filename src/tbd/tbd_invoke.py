#!/usr/bin/python

import sys
import re
import csv
import traceback
import tbd 

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 8 :
   print "usage: " + program_name + " <debug_level : 1-4> <isin-bse.csv> <isin-nse.csv> <plan.csv> <demat.csv>... "
   sys.exit(1) 

debug_level = int(sys.argv[1])
isin_bse_filename = sys.argv[2]
isin_nse_filename = sys.argv[3]
plan_filename = sys.argv[4]
demat_filename = sys.argv[5]

out_filename_phase1 = sys.argv[6]
out_filename_phase2 = sys.argv[7]
out_filename_phase3 = sys.argv[8]
	
if debug_level > 1 :
	print 'args :' , len(sys.argv)

tbd = tbd.Tbd()

tbd.set_debug_level(debug_level)
tbd.load_tbd_data(isin_bse_filename, isin_nse_filename, plan_filename, demat_filename)

tbd.print_tbd_phase1(out_filename_phase1)
tbd.print_tbd_phase2(out_filename_phase2)
# get only stocks not acquired in last 6 months : 180 days
tbd.print_tbd_phase3(out_filename_phase3, 180)
