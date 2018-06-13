#!/usr/bin/python

import sys
import re
import csv
import traceback
from collections import Counter
from operator import itemgetter

import demat_prep

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

demat_prep = demat_prep.Demat_Prep(debug_level, in_file, out_file_1, out_file_2, out_file_3, out_file_4)

demat_prep.load_data()
demat_prep.print_phase1()
demat_prep.print_phase2()
demat_prep.print_phase3()
demat_prep.print_phase4()
