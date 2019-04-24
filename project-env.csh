
setenv PROJECT_ROOT `pwd` 

setenv PROJ_SOURCE_LOC $PROJECT_ROOT/src
setenv PROJ_DATA_LOC  $PROJECT_ROOT/input-global-data
setenv PROJ_REPORTS_LOC $PROJECT_ROOT/output-global-reports

setenv PROJ_LOCAL_DATA_LOC  $PROJECT_ROOT/input-local-data
setenv PROJ_LOCAL_REPORTS_LOC $PROJECT_ROOT/output-local-reports

# use later
setenv PROJ_PROFILE default 

setenv PROJ_PROFILE_DATA_LOC  $PROJECT_ROOT/input-user-data
setenv PROJ_PROFILE_REPORTS_LOC $PROJECT_ROOT/output-user-reports

setenv PATH ${PROJ_SOURCE_LOC}:.:${PATH}

setenv PYTHONPATH ${PROJ_SOURCE_LOC}
setenv QUANDL_KEY `cat $HOME/quandl.key`
setenv PLOTLY_API_KEY `cat $HOME/plotly.key`


# if test "${PYTHONPATH}"  == ""
# then
# else
#  setenv PYTHONPATH ${PROJ_SOURCE_LOC}:${PYTHONPATH}
# endif
