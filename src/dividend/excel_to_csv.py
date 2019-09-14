#!/usr/bin/python

import sys

import pandas as pd

program_name = sys.argv[0]

if len(sys.argv) < 4 :
   print "usage: " + program_name + " <file.xls> <file.csv> <debug_level>"
   sys.exit(1) 

excel_file = sys.argv[1]

csv_file = sys.argv[2]

debug_level = int(sys.argv[3])

# get worksheet name
xl = pd.ExcelFile(excel_file)
print xl.sheet_names

# single worksheet - OpTransactionHistory
sheet_name = xl.sheet_names[0]

if sheet_name != 'OpTransactionHistory':
	print "check sheet name"
	sys.exit(1)

df = xl.parse(sheet_name)

# remove top 10 lines and bottom lines from dataframe
df = df.iloc[10:]

# change columns from top line
df.columns = df.iloc[0]

print df.columns

# remove the top line that contains column nmae
df = df.iloc[1:]

# remove 28 lines from bottom  : Legends data
df = df[:-28]

# TBD - later
# remove last column : Balance (INR)
# df = df.iloc[:, :-1]
# For backward compatibility
# Currently, clear the value in last column  : Balance(INR)
df['Balance (INR)'] = 0

# Add a dummy column - for backward compatibility
df[''] = ''

# Keep only ACH and CMS for dividend transfer
# remove transactions with remarks ':Int.Pd:' and 'BY CASH', MMT (IMPS), EBA etc
# Donot use single quote around ppatern for regex
pattern = "Transaction\ Remarks|ACH/|CMS/"

filter = df['Transaction Remarks'].str.contains(pattern, regex=True)

if debug_level > 0:
	print filter

df = df[filter]

df.to_csv(csv_file, header=True, index=False)
# df.to_csv(csv_file, header=False, index=False)

# df = pd.read_excel(excel_file, sheetName=None)
# print df.keys()

# pd.read_excel(excel_file).to_csv(csv_file, index=False)
