#!/usr/bin/python

import re

def normalize_comp_name(comp_name):
	comp_name = comp_name.capitalize()
        # remove hyphen (V-guard)
        comp_name = re.sub('-',' ', comp_name)
        # remove . in Dr. lal pathlabs
        comp_name = re.sub('\.','', comp_name)
        # remove ' in Dr Reddy's Laboratories
        comp_name = re.sub('\'','', comp_name)
        comp_name = re.sub('limited','', comp_name)
        comp_name = re.sub('ltd','', comp_name)
        comp_name = re.sub('india','', comp_name)
        # replace and and &
        comp_name = re.sub(' and ',' ', comp_name)
        comp_name = re.sub(' & ',' ', comp_name)
        # remove any characters after (  :
        # TRENT LTD (LAKME LTD)
        comp_name = re.sub('\(.*','', comp_name)
        # convert multiple space to single space
        comp_name = re.sub(' +', ' ', comp_name)
        return comp_name
