#!/usr/bin/python

import sys
import re
import csv
import traceback
from collections import Counter
from operator import itemgetter

import demat

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 3:
    print
    "usage: " + program_name + " <debug_level : 1-4> <demat.csv> ... "
    sys.exit(1)

debug_level = int(sys.argv[1])
in_filename = sys.argv[2]

if debug_level > 1:
    print
    'args :', len(sys.argv)

comp_name = 'All'

if len(sys.argv) == 4:
    comp_name = sys.argv[3]
    comp_name = comp_name.capitalize()

demat_obj = demat.Demat(debug_level, in_filename)

demat_obj.load_data()

if comp_name == "All":
    print
    'companies count : ', demat_obj.size_buy_data()
    demat_obj.print_comp_data()
else:
    print
    'Quantity : ', demat_obj.get_comp_quantity(comp_name)
    print
    'Units : ', demat_obj.get_comp_units(comp_name)
