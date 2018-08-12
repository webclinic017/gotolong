# In-Stock-Screener

An Indian Stock Screener can be used to identify stocks for buy and sale.

The tool is depdendant on things like AMFI data to figure out cap (small, mid, large etc). To be automated for refresh every 6 month.

The tool is also dependent on ISIN data from BSE/NSE. Already loaded. To be automated for refresh.

The tool is also dependent on screener data for some interesting ratios. Trying to figure out how to load it at one shot for BSE/NSE 500 companies.

The tool is also dependent on mstar (morning star) data. Yet to be integrated.

The user has to provide following information.

Currently, user has to prepare a plan-data sheet under profile/ directory : create .xls file and save it as .csv file.

The default user-profile is surinder.

The user also has to provide icidirect demat data (portfolio detailed summary).


# AMFI Data
The file data/amfi-data/amfi-\*.csv has a list of companies with market cap and cap type released every 6 months (In July for Jan-Jun).
These are downloaded from the amfi website and processed further.

Fix discrepancy

$ cd src/amfi

$ ./amfi_invoke.sh

Review the generated reports/amfi-reports/\*.csv

The report has important things like ISIN Number, Company name, Company Rank By mcap, mcap (avg of 6 months) and cap type (large, mid cap and small cap).

# ISIN Data

The file data/isin-data/isin-(bse|nse)-500.csv has a list of BSE 500 and NSE 500 companies with ISIN number.
These were downloaded directly from the NSE and BSE websites.

Fix discrepancy

  $ cd src/isin
  
  $ ./isin_invoke.sh
  
Review the generated reports/isin-reports/\*.csv


 # SCREENER Data
 
 Create a watchlist of companies (from plan data) with interesting columns.
 
 Download the screener data in data/screener-data/\*.csv
 
 Generate screener reports using
 
 $ cd src/screener
 
 $ ./screener_invoke.sh
 
 Review the generated reports/screener-reports/\*.csv files
 
 NOTE: To be switched to Quandl or something similar.

 # Morning Star Data

 $ cd src/mstar
 
 $ ./mstar_invoke.sh

Review the generated reports/mstar-reports/\*.csv

Useful to analyze moat rating (wide, narrow), Valuation Rating (Undervalued, Fairly Valued, Overvalued) 
and financial strength (Strong, Moderate etc)

# PLAN DATA

Prepare data/plan-data/plan-data.csv file

Include weight for each company and cummulative weight for industry.

1 Unit can be represented by 1000 Rs.
0 Unit : stock is under watch but there is no plan to acquire it right now.

Industry name,  Company, Space, Company name (First), Company name (Second), Company name (Third)
Space,          Details, Industry Details,
Space,          Units, <cummuulative units>, Unit (First), Unit (Second), Unit (Third)


NOTE: Try to use just first two words for the company name if that will make it unique in BSE 500.

Fix any discrepancy by running following

 $ cd src/plan
 
 $ ./plan_invoke.sh

Review the generated profile/default/reports/plan-reports/\*.csv

The summary lines shows distribution of large cap, mid cap and small cap.
TBD : Include line for micro cap and nano cap.


# DEMAT DATA

Download demat data from ICICI Direct (all holdings, all txns in csv format) in data/demat-data/demat-data.csv 

Fix any discrepancy by running following

 $ cd src/demat
 
 $ ./demat_invoke.sh
 
 Review the generated profile/default/reports/demat-reports/\*.csv files
 


 # TBD Data (To Be Done)
  
To know units to be acquired in this quarter (with 6 month delay : 2 Quarter delay)

Execute following

   $ cd src/tbd
   
   $ ./tbd-invoke.sh

Review the generated files profile/default/reports/tbd-reports/\*.csv


# BONUS share Data (To be modified for new framework)
# SPLITS share data (to be coded)
# DIVIDEND Data (To be modified)
