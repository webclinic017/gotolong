#!/usr/bin/python

import sys
import re
import csv
import traceback
import schema

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 3:
    print
    "usage: " + program_name + " <debug_level : 1-4> <schema.csv> ... "
    sys.exit(1)

debug_level = int(sys.argv[1])
schema_filename = sys.argv[2]
# db_filename = sys.argv[3]

if debug_level > 1:
    print
    'args :', len(sys.argv)

schema = schema.Schema()

schema.set_debug_level(debug_level)

schema.create_schema(schema_filename)
# schema.create_schema(db_filename, schema_filename)

# schema.print_phase1(out_filename)
