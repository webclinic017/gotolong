
setenv PROJECT_ROOT `pwd` 

setenv PROJ_SOURCE_LOC $PROJECT_ROOT/gotolong-loader/src
setenv PROJ_DATA_LOC $PROJECT_ROOT/gotolong-loader/data

setenv PATH ${PROJ_SOURCE_LOC}:${PROJECT_ROOT}:.:${PATH}

setenv PYTHONPATH ${PROJ_SOURCE_LOC}:${PROJECT_ROOT}
setenv QUANDL_KEY `cat $HOME/quandl.key`
setenv PLOTLY_API_KEY `cat $HOME/plotly.key`

# if test "${PYTHONPATH}"  == ""
# then
# else
#  setenv PYTHONPATH ${PROJ_SOURCE_LOC}:${PYTHONPATH}
# endif
