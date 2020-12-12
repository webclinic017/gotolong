# GotoLong

GotoLong is an Indian Stock Advisor (ISA) that can be used to identify stocks for buy and sale.
It relies on (a) investor's existing portfolio of stocks and (b) financial data of BSE-500/Nifty-500 stocks.

It is still in Beta phase and developers can experiment with it. Once it can be used by any user with basic knowledge of
computer, it will be tagged as v1.0

## Support
http://www.gotolong.in/

## Installation - steps

Download Python 3.*

Download mariadb (for DB) - used mariadb10.4

Install Django

python -m pip install Django
pip3 install Ptable

Download GitHub (includes Git-Bash)

## Installation - for development

Download PyCharm

Download HeidiSQL (crashes sometimes) : DB browser

Download VIM 

Download DropBox/OneDrive/GoogleDrive or something else to store the input data and output reports.

## Pull the github repository

Pull the github repository

git clone https://github.com/surinder432/gotolong


## Install Database schema
The db schema is in {GOTOLONG_DATA}/db-schema/ directory.

Create the database schema.

## Configuration

For DB name, user and password

Modify top level : 

gotolong-filter.ini

Currently, it is used by non django loaders of most modules.


## Input Data 

### user scope
Gather and store files like demat summary and demat detailed data in input-user-data

## Generate report for all modules
cd {GOTOLONG_DATA}/

./config.sh

{GOTOLONG_DATA}/src/all_reports.sh

## Explore the reports (.csv files)

Check following directory

{GOTOLONG_DATA}/output-user-reports

## Explore the reports using web browser

### Django DB config

Modify django config file for DB name, user name and password :

${GOTOLONG_DATA}/src-django-proj-root/mysite/settings.py

### Django Web Server

The django project is capable of browsing the data stored in 'gotolong' database. 

The migration from offline files to the web interface is still work-in-progress

cd ${GOTOLONG_DATA}/src-django-proj-root/

python manage.py runserver

Starting development server at http://127.0.0.1:8000/

### Web browser : URL

Use the following URL to browse the reports

http://127.0.0.1:8000/

## Code Modules Description

## amfi module

mapping of ticker and mcap and captype

## isin module

mapping of ticker and ISIN

## Giving Back Score

Module : bse -> corpact

## 52-week high and low and CMP (yesterday)

Modules : bhav, ftwhl, nse

## demat module (icici direct portfolio)

demat transaction details

demat summary details

Module name : demat 

## screener module

financial data of bse 500 for 10 years

## trendlyne module

for broker average target of healthy stocks

## global weight module

assign weight by captype

user weight is not used right now

Name : global_weight

## phealth module

identify companies at healthy price

Dependency : 

## dividend module

create dividend matrix by company and month.

Dependency : nach -> dividend