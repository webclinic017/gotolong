#!/usr/bin/python

import sys

import pandas as pd

program_name = sys.argv[0]

if len(sys.argv) < 5:
    print("usage: " + program_name + " <bank> <file.xls> <file.csv> <debug_level>")
    sys.exit(1)

bank_name = sys.argv[1]

excel_file = sys.argv[2]

csv_file = sys.argv[3]

debug_level = int(sys.argv[4])

# get worksheet name
xl = pd.ExcelFile(excel_file)

if debug_level > 0:
    print(xl.sheet_names)

# single worksheet - OpTransactionHistory
sheet_name = xl.sheet_names[0]

if bank_name == 'icici-bank':
    if sheet_name != 'OpTransactionHistory':
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

if bank_name == 'icici-bank':
    # remarks - description
    df.columns = (
        'ignore_0', 'serial_num', 'value_date', 'txn_date', 'ref_cheque_num', 'txn_description', 'withdraw_amount',
                  'deposit_amount', 'balance')
elif bank_name == 'sbi-bank':
    # credit -> deposit
    # debit -> withdraw
    df.columns = ('txn_date', 'value_date', 'txn_description', 'ref_cheque_num', 'withdraw_amount', 'deposit_amount',
                  'balance')
elif bank_name == 'hdfc-bank':
    # narration -> description
    df.columns = ('txn_date', 'txn_description', 'ref_cheque_num', 'value_date', 'withdraw_amount', 'deposit_amount',
                  'balance')
elif bank_name == 'axis-bank':
    # SRL NO, Tran Date, CHQNO, PARTICULARS, DR, CR, BAL, SOL
    df.columns = ('serial_num', 'txn_date', 'ref_cheque_num', 'txn_description', 'withdraw_amount', 'deposit_amount',
                  'balance', 'sol')
else:
    print('unsupported bank: please configure df.columns')

# TODO : Remove lines in case last column is null. Use -1 instead
# if bank_name == 'icici-bank':
# Keep only if 'Balance (INR)' column is not NA
#    df = df[df['Unnamed: 8'].notnull()]
# elif bank_name == 'sbi-bank':
#    # Keep only if 'Balance' column is not NA
#    df = df[df['Unnamed: 6'].notnull()]
# elif bank_name == 'hdfc-bank':
#    # Keep only if 'Closing Balance' column is not NA
#    df = df[df['Unnamed: 6'].notnull()]

# keep only if balance is non-null
df = df[df['balance'].notnull()]

# txn_description is non-null
df = df[df['txn_description'].notnull()]

# select only the required columns : txn date, description and deposit amount
df = df[['txn_date', 'txn_description', 'deposit_amount']]

# invalid data processing
if bank_name == 'icici-bank':
    # first line is 'Transaction Date from' : case sensitive
    # df = df[df['Unnamed: 1'] != 'Transaction Date from']
    print('not used now : Transaction Date from')

# first column processing
if bank_name == 'icici-bank':
    # remove first column (NaN before S.No) - axis 1 is column, 0 is row
    # df.drop(df.columns[0], axis=1, inplace=True)
    print('no longer need to remove first column explicitly')

if bank_name == 'icici-bank' or bank_name == 'sbi-bank':
    # remove last column : Balance (INR) - ICICI
    # remove last column : Balance - SBI
    # df = df.iloc[:, :-1]
    print('no longer need to remove last column explicitly')

# change columns from second line from top
# df.columns = df.iloc[0]

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

pattern = "ACH/|CMS/"
filter = df['txn_description'].str.contains(pattern, regex=True)

if debug_level > 0:
    print(filter)

df = df[filter]

# fix formatting for date : dd-mm-yy to dd/mm/yy
# for any bank like SBI bank
df['txn_date'] = df['txn_date'].replace({'-': '/'})

# TODO: how to convert mmm to mm ?
# TODO: how to convert yy to yyyy

# if bank_name == 'icici-bank':
    # dd/mm/YYYY
# print('date already in format')
# elif bank_name == 'hdfc-bank':
    # convert dd/mm/yy to dd/mm/yyyy
    # d = datetime.datetime.strptime(my_date, '%d/%m/%y')
    # d.strftime('%d/%m/%Y')
    # df['txn_date'] = df['txn_date'].dt.strftime('%d/%m/%Y')
# print('try to convert yy to yyyy')
# elif bank_name == 'sbi-bank':
    # convert dd-mmm-yy to dd/mm/yyyy
    # d = datetime.datetime.strptime(my_date, '%d-%b-%y')
    # d.strftime('%d/%m/%Y')
    # df['txn_date'] = df['txn_date'].dt.strftime('%d/%m/%Y')
# print('convert dd-mmm-yy to dd/mm/yyyy')


if debug_level > 0:
    print(df)

df.to_csv(csv_file, header=True, index=False)

# df.to_csv(csv_file, header=False, index=False)

# df = pd.read_excel(excel_file, sheetName=None)
# print df.keys()

# pd.read_excel(excel_file).to_csv(csv_file, index=False)
