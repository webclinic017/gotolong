#!/usr/bin/python

import sys
import re
import csv
import traceback
import plan

from operator import itemgetter


# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 6 :
   print "usage: " + program_name + " <debug_level : 1-4> <amfi.csv> <plan.csv> ... "
   sys.exit(1) 

debug_level = int(sys.argv[1])
in_plan_filename = sys.argv[2]
out_filename_phase1 = sys.argv[3]
out_filename_phase2 = sys.argv[4]
out_filename_phase3 = sys.argv[5]
out_filename_phase4 = sys.argv[6]
out_filename_phase5 = sys.argv[7]
	
if debug_level > 1 :
	print 'args :' , len(sys.argv)

indu_comp = 'comp'
ic_name = 'all'

if len(sys.argv) == 9 :
	indu_comp = sys.argv[5]
	ic_name = sys.argv[6]
	ic_name = ic_name.capitalize()

plan = plan.Plan()

plan.set_debug_level(debug_level)

plan.load_amfi_db()
plan.load_plan_data(in_plan_filename)

plan.plan_dump_ticker(out_filename_phase1)
plan.plan_dump_sorted_units(out_filename_phase2)
plan.plan_dump_all(out_filename_phase3)
plan.plan_dump_plus(out_filename_phase4)
plan.plan_dump_zero(out_filename_phase5)

if len(sys.argv) == 8 :
	if indu_comp.lower() == "comp":
		print 'companies count : ', plan.size_comp_data()
		if ic_name == "All":
			plan.print_comp_data()
		else:
			print plan.get_plan_comp_units(ic_name)
	else:
		print 'industries count : ', plan.size_indu_data()
		if ic_name == "All":
			plan.print_indu_data()
		else:
			print plan.get_indu_units(ic_name)
