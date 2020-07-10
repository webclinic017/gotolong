# GotoLong

An Indian Stock Screener can be used to identify stocks for buy and sale.

## Support
http://www.gotolong.in/

## Pull the github repository

Pull the github repository

git clone https://github.com/surinder432/gotolong


## Install Database schema
The db schema is in {GOTOLONG_HOME}/db-schema/ directory.

Create the database schema.

## Configuration

For DB name, user and password

Modify top level : 

config.ini

Currently, it is used by non django loaders of most modules.


## Input Data 

### user scope
Gather and store files like bank statement, demat summary and
demat detailed data in input-user-data

## Generate report for all modules
cd {GOTOLONG_HOME}/

./config.sh

{GOTOLONG_HOME}/src/all_reports.sh

## Explore the reports using web browser

### Django DB config
Modify django config file for DB name, user name and password : 
${GOTOLONG_HOME}/src/django-proj-root/mysite/settings.py

### Django Web Server
The django project is capable of browsing the data stored
in 'gotolong' database. The migration from offline files to the
web interface is still in progress

cd ${GOTOLONG_HOME}/src/django-proj-root/

python manage.py runserver

Use the URL given here to browse the reports.

## Code Modules Description

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