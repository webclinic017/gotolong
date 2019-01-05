#!/bin/sh

DIV_NAME=${PROJ_PROFILE_REPORTS_LOC}/dividend-reports/all/all-name_only.csv
PLAN_NAME=${PROJ_PROFILE_REPORTS_LOC}/plan-reports/plan-reports-sort-name.csv

mkdir -p ${PROJ_PROFILE_REPORTS_LOC}/review-reports

comm -13 ${DIV_NAME} ${PLAN_NAME} > ${PROJ_PROFILE_REPORTS_LOC}/review-reports/review_plan_plus_dividend_none.txt

# should be done later
# comm -23 ${DIV_NAME} ${PLAN_NAME} > ${PROJ_PROFILE_REPORTS_LOC}/review-reports/review_plan_none_dividend_plus.txt

# comm -13 ${PROJ_REPORTS_LOC}/dividends/all/all-name_only.csv ${PROJ_REPORTS_LOC}/targets/all/all-company_name_only.txt > $PROJ_REPORTS_LOC/decisions/all/decision_holdings_plus_dividend_zero.txt

# comm -23 ${PROJ_REPORTS_LOC}/dividends/all/all-name_only.csv ${PROJ_REPORTS_LOC}/targets/all/all-company_name_only.txt > $PROJ_REPORTS_LOC/decisions/all/decision_dividend_plus_holdings_zero.txt

