#!/usr/bin/python

import sys
import re
import csv
import traceback
import tbd 

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 6 :
   print "usage: " + program_name + " <debug_level : 1-4> <plan.csv> <demat.csv>... "
   sys.exit(1) 

debug_level = int(sys.argv[1])
plan_filename = sys.argv[2]
demat_filename = sys.argv[3]

out_filename_phase1 = sys.argv[4]
out_filename_phase2 = sys.argv[5]
out_filename_phase3 = sys.argv[6]
	
if debug_level > 1 :
	print 'args :' , len(sys.argv)

tbd = tbd.Tbd()

tbd.set_debug_level(debug_level)
tbd.load_tbd_data(plan_filename, demat_filename)

tbd.print_tbd_phase1(out_filename_phase1)
tbd.print_tbd_phase2(out_filename_phase2)
# get only stocks not acquired in last 6 months : 180 days
tbd.print_tbd_phase3(out_filename_phase3, 180)

