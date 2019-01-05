
setenv PROJECT_ROOT `pwd` 

setenv PROJ_SOURCE_LOC $PROJECT_ROOT/src
setenv PROJ_DATA_LOC  $PROJECT_ROOT/resources/global/data
setenv PROJ_REPORTS_LOC $PROJECT_ROOT/resources/global/reports

setenv PROJ_LOCAL_DATA_LOC  $PROJECT_ROOT/resources/local/data
setenv PROJ_LOCAL_REPORTS_LOC $PROJECT_ROOT/resources/local/reports

setenv PROJ_PROFILE default 

setenv PROJ_PROFILE_DATA_LOC  $PROJECT_ROOT/resources/profile/$PROJ_PROFILE/data
setenv PROJ_PROFILE_REPORTS_LOC $PROJECT_ROOT/resources/profile/$PROJ_PROFILE/reports

setenv PATH ${PROJ_SOURCE_LOC}:.:${PATH}

setenv PYTHONPATH ${PROJ_SOURCE_LOC}
setenv QUANDL_KEY `cat $HOME/quandl.key`
setenv PLOTLY_API_KEY `cat $HOME/plotly.key`


# if test "${PYTHONPATH}"  == ""
# then
# else
#  setenv PYTHONPATH ${PROJ_SOURCE_LOC}:${PYTHONPATH}
# endif
