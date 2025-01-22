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

if i2cdetect -y 1 | grep -q " 3c "; then
    # I2C OLED display at address 0x3c is present
    if [ "$1" = "wlan0" ]; then
        if [ "$2" = "down" ] || [ "$2" = "up" ]; then
            if ! pgrep -f systemDisplay.py > /dev/null; then
                /home/jdn/Code/HeadlessRasPi/src/systemDisplay.py
            else
                logger -t systemDisplay "Another instance is already running"
            fi
        fi
    fi
else
    logger -t systemDisplay "I2C device at address 0x3c is not found"
    exit 1
fi
exit 0
