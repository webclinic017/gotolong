#!/usr/bin/python

import sys
import re
import csv
import traceback
import plan

from operator import itemgetter


# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 5 :
   print "usage: " + program_name + " <debug_level : 1-4> <amfi.csv> <plan.csv> ... "
   sys.exit(1) 

debug_level = int(sys.argv[1])
in_amfi_filename = sys.argv[2]
in_plan_filename = sys.argv[3]
out_filename_phase2 = sys.argv[4]
out_filename_phase3 = sys.argv[5]
out_filename_phase4 = sys.argv[6]
	
if debug_level > 1 :
	print 'args :' , len(sys.argv)

indu_comp = 'comp'
ic_name = 'all'

if len(sys.argv) == 8 :
	indu_comp = sys.argv[5]
	ic_name = sys.argv[6]
	ic_name = ic_name.capitalize()

plan = plan.Plan()

plan.set_debug_level(debug_level)

plan.load_amfi_data(in_amfi_filename)
plan.load_plan_data(in_plan_filename)

plan.print_phase2(out_filename_phase2)
plan.print_phase3(out_filename_phase3)
plan.print_phase4(out_filename_phase4)

if len(sys.argv) == 7 :
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
