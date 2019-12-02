
Include the zero holdings also for statistics.

# Steps to use the script :
# 1> Login to ICICIDirect site
# 2> Trade & Invest -> Portfolio & Statements  (https://secure.icicidirect.com/IDirectTrading/Trading/Trade.aspx)
# 3> Portfolio -> Equity
# 4.1> Grouping : All (to cover zero and negative holdings)
# 4.2> Equity Portfolio Tracker (top right) -> Advanced options
# 5> Download : All Transaction (csv)
# 6> File : 8501317095_PortFolioEqtSummary.csv
# 7> Upload the file to github (stock-market/all-txn/) and rename it to 20180417_PortFolioEqtSummary.csv (change the date)
# 7> Here is a format of the file
# Stock Symbol,Company Name,ISIN Code,Action,Quantity,Transaction Price,Brokerage,Transaction Charges,StampDuty,Segment,STT Paid/Not Paid,Remarks,Transaction Date,Exchange,
# 3MIND,3M INDIA LIMITED,INE470A01017,Buy,1,13647.95,120.86,0.40,0.00,Rolling,STT Paid,icicidirect,11-Jul-2017,BSE,
