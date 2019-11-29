
#!/bin/sh

DEBUG_LEVEL=1

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`


CHEALTH=chealth

# equity user
for EUSER in nifty demat normal
do
    echo "generating reports for equity user ${EUSER}"

    EUDIR=user-${EUSER}

    if test "${EUSER}" == "demat"
    then
        IN_FILE_1=$CONFIG_PROFILE_REPORTS_LOC/demat-reports/demat-reports-ticker-only.csv
    else
        IN_FILE_1=$CONFIG_PROFILE_DATA_LOC/${CHEALTH}-data/${EUDIR}/${EUDIR}-ticker-list.csv
    fi

    IN_FILE_2=$CONFIG_REPORTS_LOC/screener-reports/screener-reports-fltr-buy-ticker-only.csv

    IN_FILE_3=$CONFIG_REPORTS_LOC/screener-reports/screener-reports-fltr-hold-ticker-cause.csv

    IN_FILE_4=$CONFIG_REPORTS_LOC/screener-reports/screener-reports-fltr-sale-ticker-cause.csv

    OUT_DIR=$CONFIG_PROFILE_REPORTS_LOC/${CHEALTH}-reports/${EUDIR}/

    mkdir -p ${OUT_DIR}

    # present in file 1 (ticker list) only - (not in screener - hold and buy ) recommendation - drop from portfolio
    OUT_FILE_1=${OUT_DIR}/reco-sale.csv

    # present in file 2 (screener - buy) only - recommendation - add
    OUT_FILE_2=${OUT_DIR}/reco-buy-new.csv

    # present in both file 1 and file 2 (screener - buy)  - recommendation - more
    OUT_FILE_3=${OUT_DIR}/reco-buy-more.csv

    # present in both file 1 and file 2 (screener - hold)  - recommendation - keep - hold
    OUT_FILE_4=${OUT_DIR}/reco-hold.csv

    # reco - none - as data missing
    OUT_FILE_5=${OUT_DIR}/reco-none.csv

    # python -m pdb weight_invoke.py ${DEBUG_LEVEL} ${IN_FILE_PLAN} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5}
    python chealth.py ${DEBUG_LEVEL} ${IN_FILE_1} ${IN_FILE_2} ${IN_FILE_3} ${IN_FILE_4} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5}

    echo "generated reports for equity user ${EUSER}"
done
