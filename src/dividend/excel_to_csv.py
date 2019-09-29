#!/usr/bin/python

import sys

import pandas as pd

program_name = sys.argv[0]

if len(sys.argv) < 4 :
   print("usage: " + program_name + " <file.xls> <file.csv> <debug_level>")
   sys.exit(1) 

excel_file = sys.argv[1]

csv_file = sys.argv[2]

debug_level = int(sys.argv[3])

# get worksheet name
xl = pd.ExcelFile(excel_file)

if debug_level > 0:
	print(xl.sheet_names)

# single worksheet - OpTransactionHistory
sheet_name = xl.sheet_names[0]

if sheet_name != 'OpTransactionHistory' :
	print("check sheet name")
	sys.exit(1)

df = xl.parse(sheet_name)

# find index of 'Transactions List -' in Unnamed:1 column
# top_index = map(lambda x: x.find('Transactions List -'), df['Unnamed: 1'])

# print("top_index : " + str(top_index))
# find index of 'Legends Used in Account Statement' in Unnamed:1 column
# bottom_index = map(lambda x: x.find('Legends Used in Account Statement'), df['Unnamed: 1'])

# print("bottom_index : " + str(bottom_index))

# remove top 11 lines (ignore logo) from dataframe
# df = df.iloc[top_index:]

# remove 28 lines from bottom  : exclude Legends data
# df = df[:bottom_index-1]

# Keep only if Transaction Remarks column is not NA
df = df[df['Unnamed: 5'].notnull()]

# first line is 'Transaction Date from' : case sensitive
df = df[df['Unnamed: 1'] != 'Transaction Date from']

# remove first column (NaN before S.No) - axis 1 is column, 0 is row
df.drop(df.columns[0], axis=1, inplace=True)

# remove last column : Balance (INR)
df = df.iloc[:, :-1]

# change columns from second line from top
df.columns = df.iloc[0]

if debug_level > 0:
	print("columns : " + df.columns)

# remove the top line that contains column name
df = df.iloc[1:]

# For backward compatibility
# Currently, clear the value in last column  : Balance(INR)
# df['Balance (INR)'] = 0

# Add a dummy column - for backward compatibility
# df[''] = ''

# Keep only ACH and CMS for dividend transfer
# remove transactions with remarks ':Int.Pd:' and 'BY CASH', MMT (IMPS), EBA etc
# Donot use single quote around ppatern for regex
pattern = "Transaction\ Remarks|ACH/|CMS/"

filter = df['Transaction Remarks'].str.contains(pattern, regex=True)

if debug_level > 0:
	print(filter)

df = df[filter]

df.to_csv(csv_file, header=True, index=False)
# df.to_csv(csv_file, header=False, index=False)

# df = pd.read_excel(excel_file, sheetName=None)
# print df.keys()

# pd.read_excel(excel_file).to_csv(csv_file, index=False)
