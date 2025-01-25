#!/bin/bash
#
# Run the script to trigger the information display when a udev event occurs
#

export WORKON_HOME=/home/jdn/.virtualenvs
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
workon WIFI

python3 /home/jdn/Code/HeadlessRasPi/src/infoDisplay.py

logger -t systemDisplay "triggerDisplay.py exited"
