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

export WORKON_HOME=/home/jdn/.virtualenvs
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
workon WIFI

sudo python3 ${HOME}/Code/HeadlessRasPi/scripts/triggerDisplay.py

logger -t systemDisplay "triggerDisplay.py exited"
