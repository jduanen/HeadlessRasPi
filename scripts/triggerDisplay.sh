#!/bin/bash
#
# Run the script to trigger the information display when a button is pushed
# 
# Run this at system startup:
#  * sudo ex ~/.config/wayfire.ini
#    - [autostart]
#      startup_script = ${HOME}/Code/HeadlessRasPi/scripts/triggerDisplay.sh
#  * chmod +x ${HOME}/Code/HeadlessRasPi/scripts/triggerDisplay.sh
#

#sudo -u jdn << EOF
export WORKON_HOME=/home/jdn/.virtualenvs
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
workon WIFI

cd /home/jdn/Code/HeadlessRasPi/scripts/
python3 ./triggerDisplay.py

logger -t systemDisplay "triggerDisplay.py exited"
#EOF
