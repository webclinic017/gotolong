#!/bin/sh

comm -13 ${PROJ_REPORTS_LOC}/dividends/all/all-name_only.csv ${PROJ_REPORTS_LOC}/targets/all/all-company_name_only.txt > $PROJ_REPORTS_LOC/decisions/all/decision_holdings_plus_dividend_zero.txt

comm -23 ${PROJ_REPORTS_LOC}/dividends/all/all-name_only.csv ${PROJ_REPORTS_LOC}/targets/all/all-company_name_only.txt > $PROJ_REPORTS_LOC/decisions/all/decision_dividend_plus_holdings_zero.txt

