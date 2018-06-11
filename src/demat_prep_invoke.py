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

if len(sys.argv) < 3 :
   print "usage: " + program_name + " <debug_level : 1-4> <demat.csv> ... "
   sys.exit(1) 

debug_level = int(sys.argv[1])
in_filename = sys.argv[2]
	
if debug_level > 1 :
	print 'args :' , len(sys.argv)

demat_prep = demat_prep.Demat_Prep(debug_level, in_filename)

demat_prep.load_data()

