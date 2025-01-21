#!/bin/bash
#
# Present system info on the I2C-connected OLED display whenever the WiFi's state changes
# 
# move this and make it executable
#   'sudo mv wifiStateChange.sh /etc/NetworkManager/dispatcher.d/90wifi-state-change.sh'
#   'sudo chmod +x /etc/NetworkManager/dispatcher.d/90wifi-state-change.sh'
#

export WORKON_HOME=/home/jdn/.virtualenvs
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
workon WIFI

if [ "$1" = "wlan0" ]; then
    echo "WiFi state changed to $2" >> /tmp/wifi_log.txt
    #if [ "$2" = "up" ] || [ "$2" = "down" ]; then
    /home/jdn/Code/HeadlessRasPi/src/systemDisplay.py
    echo "DONE\n" >> /tmp/wifi_log.txt
fi
