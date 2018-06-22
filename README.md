# Indian-stock-market (Dividend, Bonus, Plan, Demat)

The tool uses plan data (stocks to be acquired) and existing holding (stocks already acquired) to generate Quarterly reports on stocks to be acquired in the quarter with 6-month delay (can be customized).

1. isin-data/isin-(bse|nse)-500.csv has a list of BSE 500 and NSE 500 companies with ISIN number.
Downloaded directly from the websites.

Fix discrepancy

  $ cd src/isin
  $ ./isin_invoke.sh
  
2. Prepare data/plan-data/plan-data.csv file

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
 
3. Download demat/demat-data/demat-data.csv from ICICI Direct (all holdings, all txns in csv format)

Fix any discrepancy by running following

 $ cd src/demat
 $ ./demat_invoke.sh

 
  
4. To know units to be acquired in this quarter (with 6 month delay : 2 Quarter delay)
   Execute following

   $ cd src/tbd
   $ ./tbd-invoke.sh
