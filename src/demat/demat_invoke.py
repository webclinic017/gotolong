#!/usr/bin/python

import sys
import re
import csv
import traceback

import demat

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 6 :
   print "usage: " + program_name + " <debug_level : 1-4> <demat.csv> ... "
   sys.exit(1) 

debug_level = int(sys.argv[1])
in_file = sys.argv[2]
out_file_1 = sys.argv[3]
out_file_2 = sys.argv[4]
out_file_3 = sys.argv[5]
out_file_4 = sys.argv[6]
	
if debug_level > 1 :
	print 'args :' , len(sys.argv)

demat = demat.Demat()

demat.set_debug_level(debug_level)
demat.load_demat_data(in_file)
demat.print_phase1(out_file_1)
demat.print_phase2(out_file_2)
demat.print_phase3(out_file_3)
demat.print_phase4(out_file_4)
