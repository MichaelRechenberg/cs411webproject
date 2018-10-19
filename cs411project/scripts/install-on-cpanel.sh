#!/bin/bash

#
# Setup the virtual environment to be hosted on cPanel
#

#
# Assumes the following environment variables have been filled out before calling this script
#
# GIT_HOME_DIR -> The absolute path to where the root folder for the git repository
# CPANEL_VENV_ACTIVATE -> The absolute path to the 'activate' binary for the virtualenv created
#                               within the cPanel interface during "Setup Python App"
#

if [ -z "$GIT_HOME_DIR" ];
then
        echo "GIT_HOME_DIR is not set. Set it and try re-running this install script"
        exit -1
fi

if [ -z "$CPANEL_VENV_ACTIVATE" ];
then
        echo "CPANEL_VENV_ACTIVATE is not set. Set it and try re-running this install script"
        exit -1
fi


# Source internal helper scripts
source "${GIT_HOME_DIR}/cs411project/scripts/check-errs.sh"





# Activate the virtualenv, uninstall all packages and then re-install them using the requirements.txt
source ${CPANEL_VENV_ACTIVATE}
check_errs $? "Could not activate virtualenv"

pip freeze

cd ${GIT_HOME_DIR}
echo "Uninstalling all packages in virtualenvironment"
pip freeze | xargs pip uninstall -y
check_errs $? "Failed to uninstall all packages in virtualenv"

echo "Installing files from ${GIT_HOME_DIR}/requirements.txt"
pip install -r ${GIT_HOME_DIR}/requirements.txt
check_errs $? "Failed to install packages from requirements.txt"

# Run setup.py (via pip) to build the cs411project python package (so we can do 'import cs411project.foo')
echo "Running setup.py from git repo"
pip install ${GIT_HOME_DIR}
check_errs $? "Failed to run setup.py from git repo"


# Run app.py and check for non-zero exit status to make sure the installation succeeded
python ${GIT_HOME_DIR}/app.py
check_errs $? "Smoke test with app.py failed"
echo ""
echo "Installation succeeded"
