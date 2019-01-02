# In-Stock-Screener

The user has to provide following information.

Currently, user has to prepare a plan-data sheet under profile/ directory : create .xls file and save it as .csv file.

The default user-profile is default.

The user also has to provide icidirect demat data (portfolio detailed summary).

# Project Environment

For csh
* $ source project-env.csh

For sh/bash
* $ . ./project-env.sh

# PLAN DATA

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

# DEMAT DATA

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
 

 # TBD Data (To Be Done)
  
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

# Self 250 EQ Fund 

Store the information in following location. Check the template first.

* profile/default/data/sfund/sfund-data.csv


# Self Fund & Demat Sync (Aka Self 250 Equity Fund)

To ensure that the plan data is in sync with Self EQUITY FUND.

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


# DIVIDEND Data
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
