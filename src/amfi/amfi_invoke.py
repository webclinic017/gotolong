#!/usr/bin/python

import sys
import re
import csv
import traceback
import amfi

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 4:
    print("usage: " + program_name + " <debug_level : 1-4> <amfi.csv> ... ")
    sys.exit(1)

debug_level = int(sys.argv[1])
in_filename = sys.argv[2]
out_filename = sys.argv[3]

if debug_level > 1:
    print('args :', len(sys.argv))

amfi = amfi.Amfi()

amfi.set_debug_level(debug_level)

amfi.amfi_load_data(in_filename)

amfi.print_phase1(out_filename)
