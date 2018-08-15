# In-Stock-Screener

An Indian Stock Screener can be used to identify stocks for buy and sale.

The tool is depdendant on things like AMFI data to figure out cap (small, mid, large etc). 
* currently loaded manually. 
* To be automated for refresh every 6 month.

The tool is also dependent on BSE 500 and NSE 500 ISIN data.
* currently loaded manually
* Needs to be automated for refresh.

The tool is also dependent on screener data for some interesting ratios. Trying to figure out how to load it at one
shot for BSE/NSE 500 companies.

The tool is also dependent on mstar (morning star) data. Yet to be integrated.

The user has to provide following information.

Currently, user has to prepare a plan-data sheet under profile/ directory : create .xls file and save it as .csv file.

The default user-profile is default.

The user also has to provide icidirect demat data (portfolio detailed summary).

# Project Environment

For csh
* $ source project-env.csh

For sh/bash
* $ . ./project-env.sh

# AMFI Data

The file data/amfi-data/amfi-\*.csv has a list of companies with market cap and cap type released every 6 months (In July for Jan-Jun).

These are downloaded from the amfi website and processed further.

Fix discrepancy

$ cd src/amfi

$ ./amfi_invoke.sh

Review the generated report file
* reports/amfi-reports/\*.csv

The report has important things like ISIN Number, Company name, Company Rank By mcap, mcap (avg of 6 months)
and cap type (large, mid cap and small cap).

# ISIN Data

The file data/isin-data/isin-(bse|nse)-500.csv has a list of BSE 500 and NSE 500 companies with ISIN number.

These were downloaded directly from the NSE and BSE websites.

Fix discrepancy

  $ cd src/isin
  
  $ ./isin_invoke.sh
  
Review the generated report file

* reports/isin-reports/\*.csv


 # SCREENER Data
 
 Create a watchlist of BSE 500 & NSE 500 companies and any other companies from plan data with interesting columns.
 
 Download the screener data in data/screener-data/\*.csv
 
 Generate screener reports using
 
 $ cd src/screener
 
 $ ./screener_invoke.sh
 
 Review the generated report file
 * reports/screener-reports/\*.csv files
 
 NOTE: To be switched to Quandl or something similar.

 # Morning Star Data

 $ cd src/mstar
 
 $ ./mstar_invoke.sh

Review the generated reports/mstar-reports/\*.csv

Useful to analyze moat rating (wide, narrow), Valuation Rating (Undervalued, Fairly Valued, Overvalued) 
and financial strength (Strong, Moderate etc)

# PLAN DATA

Prepare plan file

* profile/default/data/plan-data/plan-data.csv

Include weight for each company and cummulative weight for industry.

1 Unit can be represented by 1000 Rs.
0 Unit : stock is under watch but there is no plan to acquire it right now.

Format of the data

* Industry name,  Company, Space, Company name (First), Company name (Second), Company name (Third)
* Space,          Details, Industry Details,
* Space,          Units, <cummuulative units>, Unit (First), Unit (Second), Unit (Third)


NOTE: Try to use just first two words for the company name if that will make it unique in BSE 500.

Fix any discrepancy by running following

 $ cd src/plan
 
 $ ./plan_invoke.sh

Review the generated report file

* profile/default/reports/plan-reports/\*.csv

The summary lines shows distribution of large cap, mid cap and small cap.
TBD : Include line for micro cap and nano cap.

# DEMAT DATA

Download demat data from ICICI Direct (all holdings, all txns in csv format) in 

* profile/default/data/demat-data/icicidirect/demat-data.csv 
* profile/default/data/demat-data/zerodha/demat-data.csv 

Fix any discrepancy by running following

 $ cd src/demat
 
 $ ./demat_invoke.sh
 
 Review the generated report files 
 * profile/default/reports/demat-reports/\*.csv 
 

 # TBD Data (To Be Done)
  
To know companies (units) to buy/sale ranked by company score (price score).

Execute following

   $ cd src/tbd
   
   $ ./tbd-invoke.sh

Review the generated reports file for buy (ordered by company price score)
* profile/default/reports/tbd-reports/\*buy\*.csv

Review the generated reports file for sale (ordered by company performance score)
* profile/default/reports/tbd-reports/\*sale\*.csv


# DIVIDEND Data
Shows dividend receieved through bank account statement.

$ cd src/dividend

$ ./dividend-reports.sh

Input data
* profile/default/data/bank-txn-data/fy1718/\*OpTransactionHistory-fy1718.csv
* profile/default/data/bank-txn-data/fy1617/\*OpTransactionHistory-fy1617.csv

Output data
* profile/default/reports/dividend-reports/

# BSE Dividend BONUS share Data

Shows dividend recieved and bonus recevied in last few years through BSE/NSE directly.

* Restrict it to only BSE 500 & NSE 500
* Incorporate Share splits data also

$ cd src/bse-dividend-bonus

$ ./bse-dividend-bonus.sh

Input data (For last 3 years)
* data/bse-data/dividend/fy\*/bse-corp-action-dividend-fy\*.csv
* data/bse-data/bonus/fy\*/bse-corp-action-bonus-fy\*.csv

Output data
* reports/dividends-bonus/


