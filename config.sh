
#export PROJECT_ROOT=`pwd | sed -e"s/Google Drive/'Google Drive'/g"` 
export PROJECT_ROOT=`pwd` 
export PKG_LOC=$PROJECT_ROOT/gotolong
export PROJ_SCRIPTS_LOC=$PROJECT_ROOT/scripts
export PATH=${PROJ_SCRIPTS_LOC}:${PROJECT_ROOT}:.:${PATH}:$(dirname `which python`)/Scripts
# add excel path
export PATH=${PATH}:/c/'Program Files (x86)'/'Microsoft Office'/Office16
# add mysql PATH
export PATH=${PATH}:/c/'Program Files'/'MariaDB 10.4'/bin

export PYTHONPATH=${PROJ_SCRIPTS_LOC}:${PKG_LOC}:.:${PROJECT_ROOT}

# set the home : contains variable data : to be used by the package by user
export GOTOLONG_DATA=$PROJECT_ROOT/data

export QUANDL_KEY=`cat $HOME/quandl.key`
export PLOTLY_API_KEY=`cat $HOME/plotly.key`

# if test "${PYTHONPATH}"  == ""
# then
# else
#  setenv PYTHONPATH ${PKG_LOC}:${PYTHONPATH}
# endif
