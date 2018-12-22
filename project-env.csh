
setenv PROJECT_ROOT `pwd` 

setenv PROJ_SOURCE_LOC $PROJECT_ROOT/src
setenv PROJ_DATA_LOC  $PROJECT_ROOT/data
setenv PROJ_REPORTS_LOC $PROJECT_ROOT/reports

setenv PROJ_PROFILE default 

setenv PROJ_PROFILE_DATA_LOC  $PROJECT_ROOT/profile/$PROJ_PROFILE/data
setenv PROJ_PROFILE_REPORTS_LOC $PROJECT_ROOT/profile/$PROJ_PROFILE/reports

setenv PATH ${PROJ_SOURCE_LOC}:.:${PATH}

setenv PYTHONPATH ${PROJ_SOURCE_LOC}
setenv QUANDL_KEY `cat $HOME/quandl.key`


# if test "${PYTHONPATH}"  == ""
# then
# else
#  setenv PYTHONPATH ${PROJ_SOURCE_LOC}:${PYTHONPATH}
# endif
