# GotoLong

An Indian Stock Screener can be used to identify stocks for buy and sale.

# Pull the github repository
Pull the github repository

# ICICI Direct

Store the required data in file input-user-data/demat-data/icicidirect

$ cd demat_idirect
$ ./*.sh

# Zerodha

Store the required data in file input-user-data/demat-data/zerodha

$ cd demat_zerodha
$ ./*.sh

# Generate recommendation : Sale & Hold

$ cd chealth
$ ./*.sh

ICICIDirect: Analyze output-user-reports/chealth-reports/user-demat_idirect/
Zerodha : Analyze output-user-reports/chealth-reports/user-demat_zerodha/

# For Buy recommendation: Get margin of Safety and up from 52w low %

$ cd gfin
$ ./*.sh

Open the output file output-global-reports/gfin-reports/gfin-reports-mos.csv in vim and paste it to google sheet to analyze the data
