
#!/bin/sh

DEBUG_LEVEL=1

CONFIG_DATA_LOC=`python -m config data`
CONFIG_REPORTS_LOC=`python -m config reports`
CONFIG_PROFILE_DATA_LOC=`python -m config profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m config profile_reports`


# equity user
for EUSER in nifty demat normal
do
    echo "generating reports for equity user ${EUSER}"

    EUDIR=user-${EUSER}

    if test "${EUSER}" == "demat"
    then
        IN_FILE_1=$CONFIG_PROFILE_REPORTS_LOC/demat-reports/demat-reports-ticker-only.csv
    else
        IN_FILE_1=$CONFIG_PROFILE_DATA_LOC/uhealth-data/${EUDIR}/${EUDIR}-ticker-list.csv
    fi

    IN_FILE_2=$CONFIG_REPORTS_LOC/screener-reports/screener-reports-filtered-ticker-only.csv

    OUT_DIR=$CONFIG_PROFILE_REPORTS_LOC/uhealth-reports/${EUDIR}/

    mkdir -p ${OUT_DIR}

    # present in file 1 (ticker list) only - recommendation - drop from portfolio
    OUT_FILE_1=${OUT_DIR}/reco-drop.csv

    # present in file 2 (screener) only - recommendation - add 
    OUT_FILE_2=${OUT_DIR}/reco-add.csv

    # present in both file 1 and file 2 (screener)  - recommendation - keep
    OUT_FILE_3=${OUT_DIR}/reco-keep.csv

    # python -m pdb weight_invoke.py ${DEBUG_LEVEL} ${IN_FILE_PLAN} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5}
    python uhealth.py ${DEBUG_LEVEL} ${IN_FILE_1} ${IN_FILE_2} ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3}

    echo "generated reports for equity user ${EUSER}"
done
