# GotoLong

An Indian Stock Screener can be used to identify stocks for buy and sale.

## Pull the github repository

Pull the github repository

git clone https://github.com/surinder432/gotolong

## Configuration

Modify top level config.ini

For DB name, user and password


## Generating reports

### global scope
provide input-global-data 

### user scope
provide input-user-data

### generate report for all modules
./all_reports.sh

### check output data
check output-global-data
check output-user-data


## Modules Description

## amfi module

mapping of ticker and mcap and captype

## isin module

mapping of ticker and ISIN

## demat module

demat transaction details
demat summary details

## screener module

screener data of bse 500

## chealth module

recommendation based on healthy companies 

## trendlyne module

for broker average target of healthy stocks

## weight module

assign weight to each company

## phealth module

identify companies at healthy price

## dividend module

create dividend matrix by company and month.

## bse module

corporate action like dividend, bonus etc by company 