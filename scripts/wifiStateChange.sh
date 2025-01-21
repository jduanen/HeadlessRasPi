#!/bin/bash
#
# Present system info on the I2C-connected OLED display whenever the WiFi's state changes
# 
# move this and make it executable
#   'sudo cp ${HOME}/Code/HeadlessRasPi/scripts/wifiStateChange.sh /etc/NetworkManager/dispatcher.d/90wifi-state-change.sh'
#   'sudo chmod +x /etc/NetworkManager/dispatcher.d/90wifi-state-change.sh'
#

export WORKON_HOME=/home/jdn/.virtualenvs
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
workon WIFI

if [ "$1" = "wlan0" ]; then
    if [ "$2" = "up" ]; then
        if ! pgrep -f systemDisplay.py > /dev/null; then
            /home/jdn/Code/HeadlessRasPi/src/systemDisplay.py
        else
            logger -t systemDisplay "Another instance is already running"
        fi
    fi
fi
