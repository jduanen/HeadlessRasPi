#!/bin/bash
#
# Run the script to trigger the information display when a udev event occurs
#

export WORKON_HOME=/home/jdn/.virtualenvs
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
workon WIFI

if pgrep -f "infoDisplay.py" > /dev/null; then
    logger -t infoDisplay "infoDisplay.py already running"
else
    logger -t infoDisplay "triggerInfoDisplay.sh starting infoDisplay.py"
    python3 /home/jdn/Code/HeadlessRasPi/src/infoDisplay.py&
fi
