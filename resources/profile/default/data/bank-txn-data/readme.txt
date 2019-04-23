# Login to icici bank account using net banking
# My accounts -> Bank Accounts -> View Detailed Statement
# Transaction Date from ... maximum 1 year period
# 01-04-2017 to 31-03-2018
# Advanced Search : Transaction Type : Credit
# Get Statement
# At bottom :  Download details as XLS file
# Save it as OpTransactionHistory17-04-2018.xls (automatic name)
# Open it and Delete first 12 lines
#   ** This remove personal details information (Name and Account number)
#   ** line # 4 'Account Number'
#   ** line # 12 'Transactions list'
# Delete logo also
# Clear contents of Balance Column (Last column). Do not remove it.
# From bottom : remove all lines including Legends Used in Account Statement
# Save it as CSV (Comma delimited) (*.csv) : OpTransactionHistory17-04-2018.csv file
# Upload OpTransactionHistory17-04-2018.csv to stock-market/fy17-18/
