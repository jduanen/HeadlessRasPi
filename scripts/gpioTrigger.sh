#!/bin/bash
#
# Run the script to trigger the information display when a button is pushed.
# It sets up the venv needed to run the infoDisplay.py script, and waits until
# any other instances are finished running before starting another instance.
# In this way, the display will continuously update as long as the GPIO pin is
# held low.
# 
# Can run this at system startup:
#  * sudo ex ~/.config/wayfire.ini
#    - [autostart]
#      startup_script = ${HOME}/Code/HeadlessRasPi/scripts/triggerDisplay.sh
#  * chmod +x ${HOME}/Code/HeadlessRasPi/scripts/triggerDisplay.sh
#
# Can also use the triggerhappy thd daemon to start this
#  ????

INFO_DISPLAY="/home/jdn/Code/HeadlessRasPi/src/infoDisplay.py"

export WORKON_HOME=/home/jdn/.virtualenvs
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
workon WIFI

# test if infoDisplay is already running and wait if it is
if pgrep -f "${INFO_DISPLAY}" > /dev/null; then
  logger -t gpioTrigger "previous infoDisplay.py running, waiting"
  pgrep -f "${INFO_DISPLAY}" | xargs wait
  logger -t gpioTrigger "previous infoDisplay.py finished running"

# run infoDisplay
logger -t gpioTrigger "infoDisplay.py called"
python3 ${INFO_DISPLAY}
logger -t gpioTrigger "infoDisplay.py exited"
