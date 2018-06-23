
setenv PROJECT_ROOT `pwd` 

setenv PROJ_SOURCE_LOC $PROJECT_ROOT/src
setenv PROJ_DATA_LOC  $PROJECT_ROOT/data
setenv PROJ_REPORTS_LOC $PROJECT_ROOT/reports

setenv PATH ${PROJ_SOURCE_LOC}:${PATH}

setenv PYTHONPATH ${PROJ_SOURCE_LOC}
# if test "${PYTHONPATH}"  == ""
# then
# else
#  setenv PYTHONPATH ${PROJ_SOURCE_LOC}:${PYTHONPATH}
# endif
