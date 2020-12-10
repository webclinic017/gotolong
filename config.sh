
#export PROJECT_ROOT=`pwd | sed -e"s/Google Drive/'Google Drive'/g"` 
export PROJECT_ROOT=`pwd` 
export PROJ_SOURCE_LOC=$PROJECT_ROOT/gotolong-loader/src
export PROJ_SCRIPTS_LOC=$PROJECT_ROOT/gotolong-loader/scripts
export PATH=${PROJ_SCRIPTS_LOC}:${PROJ_SOURCE_LOC}:${PROJECT_ROOT}:.:${PATH}:$(dirname `which python`)/Scripts:/c/'Program Files (x86)'/'Microsoft Office'/Office16

export PYTHONPATH=${PROJ_SCRIPTS_LOC}:${PROJ_SOURCE_LOC}:${PROJECT_ROOT}:$(dirname `which python`)/Scripts
export QUANDL_KEY=`cat $HOME/quandl.key`
export PLOTLY_API_KEY=`cat $HOME/plotly.key`

# set the home : contains variable data : to be used by the package by user
export GOTOLONG_HOME=$PROJECT_ROOT/gotolong-home

export PATH=${PATH}:${GOTOLONG_HOME}/scripts

# if test "${PYTHONPATH}"  == ""
# then
# else
#  setenv PYTHONPATH ${PROJ_SOURCE_LOC}:${PYTHONPATH}
# endif
