# GotoLong

GotoLong is an Indian Stock Advisor (ISA) that can be used to identify stocks for buy and sale.

It relies on

(a) Financial data (last 10 year) of Top 500 (BSE-500/Nifty-500) stocks

(b) investor's existing portfolio of stocks

It is still in Beta phase and developers can experiment with it. Once it can be used by any user with basic knowledge of
computer, it will be tagged as v1.0

## Sample Deployment

Check Sample deployment on heroku.

https://gotolong.herokuapp.com/

# Quick setup on local box

## Clone repository

git clone https://github.com/surinder432/gotolong

## Software  Pre-Req

Download Python 3.*

Download mariadb (for DB) - used mariadb10.4

Download PostgreSQL (v13) - for validation with Heroku

## Install Python packages

pip -r requirements/requirements_full.txt

## Configure DATABASE_URL

Add following to ~/.profile

export MY_DATABASE_URL=mysql://root:root@localhost:3306/gotolong

export PG_DATABASE_URL=postgres://postgres:root@localhost:5432/gotolong

export HEROKU_DATABASE_URL=`heroku config:get --app gotolong DATABASE_URL`

export DATABASE_URL=$MY_DATABASE_URL

## Create DB

gotolong_db_schema_install.sh mysql create

gotolong_db_schema_install.sh pgsql create

## Import Sample Data

gotolong_db_schema_install.sh mysql import

gotolong_db_schema_install.sh pgsql import "${PG_DATABASE_URL}"

## Start using App

The django project is capable of browsing the data stored in 'gotolong' database.

cd django_gotolong/

python manage.py runserver

Starting development server at http://127.0.0.1:8000/

Use the following URL to access the stuff

http://127.0.0.1:8000/

# Heroku Deployment

Check Sample deployment

https://gotolong.herokuapp.com/

On Heroku, the clone of repository can be connected using github.

Attach postgresql database to the heroku app.

heroku login

heroku addons:create heroku-postgresql:hobby-dev

gotolong_db_schema_install.sh pgsql import "${HEROKU_DATABASE_URL}"

heroku pg:reset --confirm \<appname\> --app \<appname\>


# Modules Information

## amfi module

mapping of ticker and mcap and captype

## isin module

mapping of ticker and ISIN

## Giving Back Score

Module : bse -> corpact

## 52-week high and low and CMP

We are ok with data of yesterday as it is for investment and not for trading.

Modules : bhav, ftwhl, nse

## demat module (icici direct portfolio)

demat transaction details

demat summary details

Module name : demat

NOTE: add support for any broker.

## screener module

financial data of bse 500 for 10 years

## trendlyne module

for broker average target of healthy stocks

## gweight module

global weight module

assign weight by captype

user weight is not used right now

Name : global_weight

## fratio module

Financial Ratio module

You can specify financial ratio filters like debt to equity ratio (der)

## greco module

Global recommendation module

Uses trendlyne module and fratio module

## phealth module

identify companies at healthy price

Dependency :

## dividend module

create dividend matrix by company and month.

Dependency : nach -> dividend

# Additional Softwares

Download PyCharm

Download HeidiSQL : DB browser

Download VIM

Download GoogleDrive to store the input data and output reports.

Download Git (includes Git-Bash)