#!/usr/bin/python

import sys

import pandas as pd

program_name = sys.argv[0]

if len(sys.argv) < 4:
    print("usage: " + program_name + " <file.xls> <file.csv> <debug_level>")
    sys.exit(1)

excel_file = sys.argv[1]

csv_file = sys.argv[2]

debug_level = int(sys.argv[3])

# get worksheet name
xl = pd.ExcelFile(excel_file)

if debug_level > 0:
    print(xl.sheet_names)

# single worksheet - Data 
sheet_name = xl.sheet_names[0]

if sheet_name != 'Data':
    print("sheet name Data not found changed to", sheet_name)
    sys.exit(1)

df = xl.parse(sheet_name)

# ignore top two line : Average Market Capitalization of listed companies during the six months ended 
# remove top two line from dataframe
df = df.iloc[1:]

if debug_level > 0:
    print("old columns : ")
    print(df.columns)

# change column name of data frame 
columns_list = ['sr_no', 'name', 'isin', 'bse_symbol', 'bse_mcap',
                'nse_symbol', 'nse_mcap', 'mse_symbol', 'mse_mcap',
                'avg_mcap', 'captype']
df.columns = columns_list

if debug_level > 0:
    print("new columns : ")
    print(df.columns)

# Keep only top 1000 entries
df = df.iloc[:1000]

# round avg_mcap
# df = df.round({'avg_mcap' : 1})
# covert to numeric
# df[["avg_mcap"]] = df[["avg_mcap"]].apply(pd.to_numeric)
df[["avg_mcap"]] = df[["avg_mcap"]].astype(int)

# drop columns that are not required
skip_columns_list = ['bse_mcap', 'nse_mcap', 'mse_symbol', 'mse_mcap']
df.drop(skip_columns_list, axis=1, inplace=True)

df.to_csv(csv_file, header=True, index=False)
