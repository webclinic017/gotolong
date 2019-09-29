# Login to icici bank account using net banking
# My accounts -> Bank Accounts -> View Detailed Statement
# Transaction Date from ... maximum 1 year period
# 01-04-2017 to 31-03-2018
# Advanced Search : Transaction Type : Credit
# Get Statement
# At bottom :  Download details as XLS file
# Save it as OpTransactionHistory17-04-2018.xls (automatic name)

# 1> Automatic
# Do not store .xlsx in git directory for security.
# Use D:\Google Drive\my_personal_pack\invest\Equity\icici-bank-txn-data\in-xls
# Use D:\Google Drive\my_personal_pack\invest\Equity\icici-bank-txn-data\xls-to-csv.sh to get .csv from .xls
# It uses src/dividend/excel_to_csv.py - to get the .csv file
# Copy out-csv directory contents to D:\Google Drive\my_github\GitHub\gotolong\input-user-data\bank-txn-data
# Upload OpTransactionHistory-fy1819.csv to stock-market/fy17-18/

# 2> Manual process
# Open it and Delete first 12 lines
#   ** This remove personal details information (Name and Account number)
#   ** line # 4 'Account Number'
#   ** line # 12 'Transactions list'
# Delete logo also
# Clear contents of Balance Column (Last column). Do not remove it.
# From bottom : remove all lines including Legends Used in Account Statement
# Save it as CSV (Comma delimited) (*.csv) : OpTransactionHistory17-04-2018.csv file
# Upload OpTransactionHistory-fy1819.csv to stock-market/fy17-18/
