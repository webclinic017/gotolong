#!/usr/bin/python

import sys
import re
import csv
import traceback
import mstar

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 5 :
   print "usage: " + program_name + " <debug_level : 1-4> <mstar.csv> ... "
   sys.exit(1) 

debug_level = int(sys.argv[1])
in_filename = sys.argv[2]
out_filename_1 = sys.argv[3]
out_filename_2 = sys.argv[4]
	
if debug_level > 1 :
	print 'args :' , len(sys.argv)

mstar = mstar.Mstar()

mstar.set_debug_level(debug_level)

mstar.load_mstar_data()

mstar.filter_data_phase1()
mstar.print_phase1(out_filename_1)

mstar.filter_data_phase2()
mstar.print_phase2(out_filename_2)
