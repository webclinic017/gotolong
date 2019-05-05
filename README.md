# In-Stock-Screener

An Indian Stock Screener can be used to identify stocks for buy and sale.

The tool is dependent on things like AMFI data to figure out cap (small, mid, large etc). 
* currently loaded manually. 
* To be automated for refresh every 6 month.

The tool is also dependent on BSE 500 and NSE 500 ISIN data.
* currently loaded manually
* Needs to be automated for refresh.

The tool is also dependent on screener data for some interesting ratios. Trying to figure out how to load it at one
shot for BSE/NSE 500 companies.

The tool is also dependent on mstar (morning star) data. Yet to be integrated.

The user has to provide following information.

Currently, user has to prepare a plan-data sheet under input-user-data directory : create .xls file and save it as .csv file.

The default user-profile is default.

The user also has to provide icidirect demat data (portfolio detailed summary).

# Project Environment

For csh
* $ source config.csh


# User : PLAN DATA

Prepare plan file

Input Data
* input-user-data/plan-data/plan-data.csv

Minimum investment size : 1 Unit

0 Unit : stock is under watch but there is no plan to acquire it right now.

Format of the data for plan

* Comp_Industry ,  Comp_Name, Comp_Ticker, Comp_Weight, Comp_Desc (company description)

NOTE: Try to use just first two words for the company name if that will make it unique in BSE 500.

Generate Report

 $ cd src/plan
 
 $ ./plan_invoke.sh

Review the generated report file

Output Data
* output-user-reports/plan-reports/\*.csv

The summary lines shows distribution of large cap, mid cap and small cap.
TBD : Include line for micro cap and nano cap.

# User : DEMAT DATA

Download demat data from ICICI Direct (all holdings, all txns in csv format) in 

Input Data
* input-user-data/demat-data/icicidirect/demat-data.csv 
* input-user-data/demat-data/zerodha/demat-data.csv 

Generate Report.

 $ cd src/demat
 
 $ ./demat_invoke.sh
 
 Review the generated report files.
 
 Output Data
 * output-user-reports/demat-reports/\*.csv 
 

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
* output-user-reports/tbd-reports/\*buy\*.csv

Review the generated reports file for sale (ordered by company performance score)
* output-user-reports/tbd-reports/\*sale\*.csv

# User : SFUND Demat Sync (SURI 250 Equity Fund)

To ensure that the plan data is in sync with SURI 250 EQUITY FUND.

Input data : SURI 250 Fund data
* input-user-data/sfund-data/sfund-data.csv
   
Input data : Demat Summary data
* input-user-data/demat-data/icicidirect/demat-summary-data.csv
* input-user-data/demat-data/zerodha/demat-data.csv

Generate required reports

* $ cd src/sfund-demat/
* $ ./one.sh

Review the generated reports
* output-user-reports/sfund-demat-reports/sfund-demat-dumb-join.csv
* output-user-reports/sfund-demat-reports/sfund-demat-dumb-diff.csv


# User : DIVIDEND Data
Shows dividend receieved through bank account statement.

Input data
* input-user-data/bank-txn-data/fy1718/\*OpTransactionHistory-fy1718.csv
* input-user-data/bank-txn-data/fy1617/\*OpTransactionHistory-fy1617.csv

Generate report

$ cd src/dividend

$ ./dividend-reports.sh

Review report.

Output data
* output-user-reports/dividend-reports/

# Global : AMFI Data

The file data/amfi-data/amfi-\*.csv has a list of companies with market cap and cap type released every 6 months (In July for Jan-Jun).

These are downloaded from the amfi website and processed further.

Input Data
* input-global-data/amfi-data/amfi-\*.csv 

Generate Report

$ cd src/amfi

$ ./amfi_invoke.sh

Review the generated report file

Output Data
* output-global-reports/amfi-reports/\*.csv

The report has important things like ISIN Number, Company name, Company Rank By mcap, mcap (avg of 6 months)
and cap type (large, mid cap and small cap).

# Global : ISIN Data

The file input-global-data/isin-data/isin-(bse|nse)-500.csv has a list of BSE 500 and NSE 500 companies with ISIN number.

These were downloaded directly from the NSE and BSE websites.

Input Data
* data/isin-data/isin-(bse|nse)-500.csv


Generate Report

  $ cd src/isin
  
  $ ./isin_invoke.sh
  
Review the generated report file

Output Data
* output-global-reports/isin-reports/\*.csv


 # Global : SCREENER Data
 
 Create a watchlist of BSE 500 & NSE 500 companies and any other companies from plan data with interesting columns.
 
 Download the screener data in data/screener-data/\*.csv
 
 Input Data
 * input-global-data/screener-data/\*.csv
 
 Generate screener reports using
 
 $ cd src/screener
 
 $ ./screener_invoke.sh
 
 Review the generated report file.
 
 Output Data
 * output-globla-reports/screener-reports/\*.csv files
 
 NOTE: To be switched to Quandl or something similar.

 # Global : Morning Star Data

Input Data
* input-global-data/mstar-data/\*.csv

Generate Report

 $ cd src/mstar
 
 $ ./mstar_invoke.sh

Review the generated report

Output Data:
* output-global-reports/mstar-reports/\*.csv

Useful to analyze moat rating (wide, narrow), Valuation Rating (Undervalued, Fairly Valued, Overvalued) 
and financial strength (Strong, Moderate etc)

# Global : BSE Dividend BONUS share Data

Shows dividend recieved and bonus recevied in last few years through BSE/NSE directly.

* Restrict it to only BSE 500 & NSE 500
* Incorporate Share splits data also

Input data (For last 3 years)
* input-global-data/bse-data/dividend/fy\*/bse-corp-action-dividend-fy\*.csv
* input-globla-data/bse-data/bonus/fy\*/bse-corp-action-bonus-fy\*.csv

Generate Report

$ cd src/bse-dividend-bonus

$ ./bse-dividend-bonus.sh

Review the generated report.

Output data

* output-global-reports/dividends-bonus/

