#!/usr/bin/python

import re

def normalize_comp_name(comp_name):
	# Capitalize
	comp_name = comp_name.capitalize()

	# remove hyphen (V-guard)
	comp_name = re.sub('-',' ', comp_name)
	
	# remove . in Dr. lal pathlabs
	comp_name = re.sub('\.','', comp_name)
	
	# remove ' in Dr Reddy's Laboratories
	comp_name = re.sub('\'','', comp_name)
	
	# removed limited and india
	comp_name = re.sub('limited','', comp_name)
	comp_name = re.sub('ltd','', comp_name)
	comp_name = re.sub('india','', comp_name)
	
	# replace and and &
	comp_name = re.sub(' and ',' ', comp_name)
	comp_name = re.sub(' & ',' ', comp_name)
	
	# replace inds (for screener) 
	comp_name = re.sub('inds','', comp_name)
	
	# remove any characters after (  :
	# TRENT LTD (LAKME LTD)
	comp_name = re.sub('\(.*','', comp_name)
	
	# convert multiple space to single space
	comp_name = re.sub(' +', ' ', comp_name)
	
	# combine H D F C into HDFC
	comp_name_list = list(comp_name)
	even_char = comp_name_list[0::2]
	odd_char = comp_name_list[1::2]
	if len(set(odd_char)) == 1:
		 comp_name = str(even_char)
	
	# strip space
	comp_name = comp_name.strip()
	
	return comp_name

def get_number(num_str):
	# strip space
	num_str = num_str.strip()
	if num_str == 'NaN':
		num_str = '0'
	
	# remove comma	
	num_str = num_str.replace(',', '')

	return int(float(num_str))
