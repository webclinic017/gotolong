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


# User : PLAN DATA

Prepare plan file

Input Data
* profile/default/data/plan-data/plan-data.csv

Include weight for each company and cummulative weight for industry.

1 Unit can be represented by 1000 Rs.
0 Unit : stock is under watch but there is no plan to acquire it right now.

Format of the data

* Industry name,  Company, Space, Company name (First), Company name (Second), Company name (Third)
* Space,          Details, Industry Details,
* Space,          Units, <cummuulative units>, Unit (First), Unit (Second), Unit (Third)


NOTE: Try to use just first two words for the company name if that will make it unique in BSE 500.

Generate Report

 $ cd src/plan
 
 $ ./plan_invoke.sh

Review the generated report file

Output Data
* profile/default/reports/plan-reports/\*.csv

The summary lines shows distribution of large cap, mid cap and small cap.
TBD : Include line for micro cap and nano cap.

# User : DEMAT DATA

Download demat data from ICICI Direct (all holdings, all txns in csv format) in 

Input Data
* profile/default/data/demat-data/icicidirect/demat-data.csv 
* profile/default/data/demat-data/zerodha/demat-data.csv 

Generate Report.

 $ cd src/demat
 
 $ ./demat_invoke.sh
 
 Review the generated report files.
 
 Output Data
 * profile/default/reports/demat-reports/\*.csv 
 

 # User : TBD Data (To Be Done)
  
To know companies (units) to buy/sale ranked by company score (price score).

Input Data
* isin data
* amfi data
* screener data
* plan data
* demat data

Generate Buy and Sale Report.

   $ cd src/tbd
   
   $ ./tbd-invoke.sh

Review the generated reports file for buy (ordered by company price score)
* profile/default/reports/tbd-reports/\*buy\*.csv

Review the generated reports file for sale (ordered by company performance score)
* profile/default/reports/tbd-reports/\*sale\*.csv

# User : SFUND Demat Sync (SURI 250 Equity Fund)

To ensure that the plan data is in sync with SURI 250 EQUITY FUND.

Input data : SURI 250 Fund data
* profile/default/data/sfund/sfund-data.csv
   
Input data : Demat Summary data
* profile/default/data/demat/icicidirect/demat-summary-data.csv
* profile/default/data/demat/zerodha/demat-data.csv

Generate required reports

* $ cd src/sfund-demat/
* $ ./one.sh

Review the generated reports
* profile/default/reports/sfund-demat-reports/sfund-demat-dumb-join.csv
* profile/default/reports/sfund-demat-reports/sfund-demat-dumb-diff.csv


# User : DIVIDEND Data
Shows dividend receieved through bank account statement.

Input data
* profile/default/data/bank-txn-data/fy1718/\*OpTransactionHistory-fy1718.csv
* profile/default/data/bank-txn-data/fy1617/\*OpTransactionHistory-fy1617.csv

Generate report

$ cd src/dividend

$ ./dividend-reports.sh

Review report.

Output data
* profile/default/reports/dividend-reports/

# Global : AMFI Data

The file data/amfi-data/amfi-\*.csv has a list of companies with market cap and cap type released every 6 months (In July for Jan-Jun).

These are downloaded from the amfi website and processed further.

Input Data
* data/amfi-data/amfi-\*.csv 

Generate Report

$ cd src/amfi

$ ./amfi_invoke.sh

Review the generated report file

Output Data
* reports/amfi-reports/\*.csv

The report has important things like ISIN Number, Company name, Company Rank By mcap, mcap (avg of 6 months)
and cap type (large, mid cap and small cap).

# Global : ISIN Data

The file data/isin-data/isin-(bse|nse)-500.csv has a list of BSE 500 and NSE 500 companies with ISIN number.

These were downloaded directly from the NSE and BSE websites.

Input Data
* data/isin-data/isin-(bse|nse)-500.csv


Generate Report

  $ cd src/isin
  
  $ ./isin_invoke.sh
  
Review the generated report file

Output Data
* reports/isin-reports/\*.csv


 # Global : SCREENER Data
 
 Create a watchlist of BSE 500 & NSE 500 companies and any other companies from plan data with interesting columns.
 
 Download the screener data in data/screener-data/\*.csv
 
 Input Data
 * data/screener-data/\*.csv
 
 Generate screener reports using
 
 $ cd src/screener
 
 $ ./screener_invoke.sh
 
 Review the generated report file.
 
 Output Data
 * reports/screener-reports/\*.csv files
 
 NOTE: To be switched to Quandl or something similar.

 # Global : Morning Star Data

Input Data
* data/mstar-data/\*.csv

Generate Report

 $ cd src/mstar
 
 $ ./mstar_invoke.sh

Review the generated report

Output Data:
* reports/mstar-reports/\*.csv

Useful to analyze moat rating (wide, narrow), Valuation Rating (Undervalued, Fairly Valued, Overvalued) 
and financial strength (Strong, Moderate etc)

# Global : BSE Dividend BONUS share Data

Shows dividend recieved and bonus recevied in last few years through BSE/NSE directly.

* Restrict it to only BSE 500 & NSE 500
* Incorporate Share splits data also

Input data (For last 3 years)
* data/bse-data/dividend/fy\*/bse-corp-action-dividend-fy\*.csv
* data/bse-data/bonus/fy\*/bse-corp-action-bonus-fy\*.csv

Generate Report

$ cd src/bse-dividend-bonus

$ ./bse-dividend-bonus.sh

Review the generated report.

Output data

* reports/dividends-bonus/

