#!/usr/bin/python

import sys
import re
import csv
import traceback
import tbd 

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 15 :
   print "usage: " + program_name + " <debug_level : 1-4> <isin-bse.csv> <isin-nse.csv> <amfi.csv> <plan.csv> <demat.csv>... "
   sys.exit(1) 

debug_level = int(sys.argv[1])
isin_bse_filename = sys.argv[2]
isin_nse_filename = sys.argv[3]
amfi_filename = sys.argv[4]
screener_aliases_filename = sys.argv[5]
plan_filename = sys.argv[6]
demat_filename = sys.argv[7]
screener_filename = sys.argv[8]

cover_filename= sys.argv[9]
plan_nocond_filename = sys.argv[10]
plan_cond_filename = sys.argv[11]
plan_cond_mos_filename = sys.argv[12]
plan_tbd_cond_filename = sys.argv[13]
plan_tbd_days_nocond_filename = sys.argv[14]
plan_tbd_days_cond_filename = sys.argv[15]
plan_demat_cond_sale_filename = sys.argv[16]
days_1 = int(sys.argv[17])
days_2 = int(sys.argv[18])
mos_1 = int(sys.argv[19])
mos_2 = int(sys.argv[20])
	
if debug_level > 1 :
	print 'args :' , len(sys.argv)

tbd = tbd.Tbd()

tbd.set_debug_level(debug_level)
tbd.load_tbd_data(isin_bse_filename, isin_nse_filename, amfi_filename, screener_aliases_filename, plan_filename, demat_filename, screener_filename)

tbd.print_tbd_phase1(cover_filename)
tbd.dump_plan_nocond(plan_nocond_filename)
tbd.dump_plan_cond(plan_cond_filename)
tbd.dump_plan_cond_mos(plan_cond_mos_filename, mos_1)
tbd.dump_plan_tbd_cond(plan_tbd_cond_filename)
tbd.dump_plan_tbd_days_nocond(plan_tbd_days_nocond_filename, days_1)
tbd.dump_plan_tbd_days_cond(plan_tbd_days_cond_filename, days_1)
tbd.dump_plan_demat_cond_sale(plan_demat_cond_sale_filename)
